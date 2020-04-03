from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class RdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, webserver_sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.vpc = vpc
        self.webserver_sg = webserver_sg
        pw = core.SecretValue.plain_text("password")
        rds_instance = rds.DatabaseInstance(
            self, "Rds",
            master_username="user",
            master_user_password=pw,
            database_name="db",
            engine=rds.DatabaseInstanceEngine.MYSQL,
            vpc=vpc,
            instance_class=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2,
                ec2.InstanceSize.MICRO),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False)
        rds_instance.connections.allow_from(
            webserver_sg,
            ec2.Port.tcp(3306))
