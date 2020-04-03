import unittest
from app.core_stack import CoreStack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.core as core
import json


class StackCase(unittest.TestCase):

    def test_if_vpc_has_public_subnets(self):
        app = core.App()
        core_construct = CoreStack(app, "core")
        selected_subnets = core_construct.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PUBLIC)
        self.assertTrue(selected_subnets.has_public)

    def test_if_vpc_has_private_subnets(self):
        app = core.App()
        core_construct = CoreStack(app, "core")
        selected_subnets = core_construct.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE)
        self.assertFalse(selected_subnets.has_public)

    def test_if_dev_role_is_not_admin(self):
        app = core.App()
        CoreStack(app, "core")
        stack = app.synth()
        core_stack = stack.get_stack_by_name("core").template
        resources = core_stack['Resources']
        for resource in resources.keys():
            if str(resource).startswith("developer"):
                developer_role = resource
        self.assertNotEqual(
            "[{'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':iam::aws:policy/AdministratorAccess']]}]",
            str(resources[developer_role]['Properties']['ManagedPolicyArns']))


if __name__ == '__main__':
    unittest.main()
