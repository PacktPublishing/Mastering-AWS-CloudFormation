from aws_cdk import core
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2


class WebStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.vpc = vpc
        userdata = '''#!/bin/sh
                      yum install httpd -y
                      systemctl enable httpd
                      systemctl start httpd
                      echo "<html><head><title> Example Web Server</title></head>" >  /var/www/html/index.html
                      echo "<body>" >>  /var/www/html/index.html
                      echo "<div><center><h2>Welcome AWS $(hostname -f) </h2>" >>  /var/www/html/index.html
                      echo "<hr/>" >>  /var/www/html/index.html
                      curl http://169.254.169.254/latest/meta-data/instance-id >> /var/www/html/index.html
                      echo "</center></div></body></html>" >>  /var/www/html/index.html'''
        websrv = ec2.UserData.for_linux()
        websrv.add_commands(userdata)
        asg = autoscaling.AutoScalingGroup(self,
                                           "WebAsg",
                                           instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
                                           machine_image=ec2.AmazonLinuxImage(),
                                           vpc=vpc,
                                           vpc_subnets=ec2.SubnetSelection(subnet_group_name="Private"),
                                           min_capacity=1,
                                           max_capacity=1,
                                           user_data=websrv
                                           )
        alb = elbv2.ApplicationLoadBalancer(self,
                                            "WebLb",
                                            vpc=vpc,
                                            internet_facing=True,
                                            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public"))
        listener = alb.add_listener("WebListener",
                                    port=80)
        listener.add_targets("Target",
                             port=80,
                             targets=[asg])

        self.webserver_sg = ec2.SecurityGroup(self, "WebServerSg", vpc=vpc)
        asg.add_security_group(self.webserver_sg)
