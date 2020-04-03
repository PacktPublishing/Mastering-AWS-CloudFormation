from cfnlint import CloudFormationLintRule
from cfnlint import RuleMatch


class RdsDeletionPolicy(CloudFormationLintRule):
    """This rule is used to verify if resources AWS::RDS::DBInstance
    and AWS::RDS::DBCluster have a deletion policy set to Snapshot or Retain"""
    id = 'W9001'
    shortdesc = 'Check RDS deletion policy'
    description = 'This rule checks DeletionPolicy on RDS resources to be Snapshot or Retain'

    def match(self, cfn):
        matches = []
        resources = cfn.get_resources(["AWS::RDS::DBInstance", "AWS::RDS::DBCluster"])
        for resource_name, resource in resources.items():
            deletion_policy = resource.get("DeletionPolicy")
            path = ['Resources', resource_name]
            if not deletion_policy:
                message = f"Resource {resource_name} does not have Deletion Policy!"
                matches.append(RuleMatch(path, message))
            elif deletion_policy not in ["Snapshot", "Retain"]:
                message = f"Resource {resource_name} does not have Deletion Policy set to Snapshot or Retain!"
                matches.append(RuleMatch(path, message))
        return matches
