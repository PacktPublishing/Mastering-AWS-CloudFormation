# Drift detection

Make sure you are in this directory and run the following command.
> Note that if you have multiple profiles like me, you want to add --profile $PROFILE_NAME at the end of your command

We start with the stack creation
```bash
aws cloudformation --create-stack --stack-name iamrole --template-body file://IamRole.yaml --capabilities CAPABILITY_IAM
```
Now when we've reviewed that our stack is in sync, we can manually edit our role
```bash
ROLENAME=$(aws cloudformation describe-stack-resources --stack-name iamrole --query "StackResources[0].PhysicalResourceId" --output text)
aws iam attach-role-policy --role-name $ROLENAME --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"
```
When we run drift detection again we will find modification.
> You will not be able to delete that stack until you detach that policy from your new role
```bash
aws iam detach-role-policy --role-name $ROLENAME --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"
aws cloudformation delete-stack --stack-name iamrole
```