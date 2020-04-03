def render_ecs(input):
    ecs_definition = {}
    ecs_task_definition = {
        "TaskDefinition": {
            "Type": "AWS::ECS::TaskDefinition",
            "Properties": {
                "Family": "",  # placeholder
                "RequiresCompatibilities": ["FARGATE"],
                "ContainerDefinitions": [
                    {
                        "Name": "",  # placeholder
                        "Image": "",  # placeholder
                        "PortMappings": [
                            {
                                "ContainerPort": "",  # placeholder
                                "Protocol": "tcp"
                            }
                        ],
                        "LogConfiguration": {
                            "LogDriver": "awslogs",
                            "Options": {
                                "awslogs-group": {"Ref": "Logs"},
                                "awslogs-region": {"Ref": "AWS::Region"},
                                "awslogs-stream-prefix": ""  # placeholder
                                }
                        }
                    }
                ],
                "Cpu": "",  # placeholder
                "ExecutionRoleArn": {"Fn::ImportValue": "ExecRole"},
                "Memory": "",  # placeholder
                "NetworkMode": "awsvpc"
            }
        }
    }
    application_image = input['ApplicationImage']
    application_name = application_image.split(":")[0]
    ecs_task_definition_properties = ecs_task_definition['TaskDefinition']['Properties']
    ecs_task_definition_properties['Family'] = application_name
    ecs_task_definition_properties['ContainerDefinitions'][0]['Name'] = application_name
    ecs_task_definition_properties['ContainerDefinitions'][0]['Image'] = application_image
    ecs_task_definition_properties['ContainerDefinitions'][0]['PortMappings'][0]['ContainerPort'] = input['ApplicationPort']
    ecs_task_definition_properties['ContainerDefinitions'][0]['LogConfiguration']['Options']['awslogs-stream-prefix'] = f"{application_name}-"
    ecs_task_definition_properties['Cpu'] = str(input['CPU'])
    ecs_task_definition_properties['Memory'] = str(input['Memory'])
    ecs_task_definition['TaskDefinition']['Properties'] = ecs_task_definition_properties

    ecs_service_definition = {
        "Service": {
            "Type": "AWS::ECS::Service",
            "Properties": {
                "Cluster": {"Fn::ImportValue": "EcsCluster"},
                "DesiredCount": 0,
                "TaskDefinition": {"Ref": "TaskDefinition"},
                "LaunchType": "FARGATE",
                "NetworkConfiguration": {
                    "AwsvpcConfiguration": {
                        "SecurityGroups": [
                            {"Ref": "Sg"}
                        ],
                        "Subnets": [
                            {"Fn::ImportValue": "AppSubnet01"},
                            {"Fn::ImportValue": "AppSubnet02"}
                        ]
                    }
                }
            }
        }
    }
    ecs_service_definition_properties = ecs_service_definition['Service']['Properties']
    ecs_service_definition_properties['DesiredCount'] = input['TaskCount']
    if "NeedsBalancer" in input and input['NeedsBalancer']:
        ecs_service_definition_properties['LoadBalancers'] = [{
                "TargetGroupArn": {"Ref": "Tg"},
                "ContainerPort": str(input['ApplicationPort']),
                "ContainerName": application_name
            }]
        ecs_service_definition_properties['HealthCheckGracePeriodSeconds'] = 30

    ecs_definition['Logs'] = {
        "Type": "AWS::Logs::LogGroup",
        "Properties": {
            "LogGroupName": application_name,
            "RetentionInDays": 1
        }
    }

    ecs_definition['Sg'] = {
      "Type": "AWS::EC2::SecurityGroup",
      "Properties": {
         "GroupDescription": "Security Group",
         "VpcId": {"Fn::ImportValue": "VpcId"}
      }
    }
    if "NeedsBalancer" in input and input['NeedsBalancer']:
        ecs_definition['Sg']['Properties']['SecurityGroupIngress'] = [
            {
                "IpProtocol": "tcp",
                "FromPort": str(input['ApplicationPort']),
                "ToPort": str(input['ApplicationPort']),
                "SourceSecurityGroupId": {"Ref": "LbSg"}
            }
        ]

    ecs_definition.update(ecs_task_definition)
    ecs_definition.update(ecs_service_definition)

    return ecs_definition


def render_rds(input):
    rds_definition = {}
    return rds_definition


def render_elb(input):
    elb_definition = {}
    return elb_definition


def lambda_handler(event, context):
    response = {}
    response['requestId'] = event['requestId']
    response['status'] = "SUCCESS"
    response['fragment'] = {}

    required_properties = ["ApplicationImage", "ApplicationPort", "TaskCount", "Memory", "CPU"]
    properties = event['fragment']['Resources']['Application']['Properties']
    for req in required_properties:
        if req not in properties.keys() or not properties[req]:
            response['status'] = "FAILED"
            return response

    rds_props = {}
    rds_props['RDSEngine'] = ""
    rds_props['RDSSize'] = "db.t2.micro"
    rds_props['RDSMultiAz'] = "false"

    for key in rds_props.keys():
        if key in properties.keys() and properties[key]:
            rds_props[key] = properties[key]

    elb_props = {}
    elb_props['NeedBalancer'] = False
    elb_props['PubliclyAvailable'] = False

    for key in elb_props.keys():
        if key in properties.keys() and properties[key]:
            elb_props[key] = properties[key]

    ecs_props = {}
    ecs_props['ApplicationImage'] = properties['ApplicationImage']
    ecs_props['ApplicationPort'] = properties['ApplicationPort']
    ecs_props['TaskCount'] = properties['TaskCount']
    ecs_props['Memory'] = properties['Memory']
    ecs_props['CPU'] = properties['CPU']
    if "NeedsBalancer" in properties:
        ecs_props['NeedsBalancer'] = properties['NeedsBalancer']
    ecs_definition = render_ecs(ecs_props)
    resources = {"Resources": {}}
    resources['Resources'].update(ecs_definition)
    response['fragment'].update(resources)
    return response

