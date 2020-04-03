from aws_cdk import core
from aws_cdk.core import Fn
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam


class CoreStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # IAM section
        admin_role = iam.Role(self,
                              "admin",
                              assumed_by=iam.AccountPrincipal(Fn.ref("AWS::AccountId")))
        self.dev_role = iam.Role(self,
                            "developer",
                            assumed_by=iam.AccountPrincipal(Fn.ref("AWS::AccountId")))
        admin_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        self.dev_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess"))
        # VPC section
        self.vpc = ec2.Vpc(self,
                           "vpc",
                           cidr="10.0.0.0/16",
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           max_azs=3,
                           nat_gateways=1,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                               ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE, cidr_mask=24)
                           ])
