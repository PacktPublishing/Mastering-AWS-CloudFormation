# Understanding CloudFormation IAM permissions

Make sure you are in this directory and run the following command.
> Note that if you have multiple profiles like me, you want to add --profile $PROFILE_NAME at the end of your command

We begin with creating our dummy role without necessary permissions.
```bash
aws cloudformation create-stack \
                   --stack-name iamrole \
                   --capabilities CAPABILITY_IAM \
                   --template-body file://IamRole.yaml
```
We obtain STS credentials for that role
```bash
IAM_ROLE_ARN=$(aws cloudformation describe-stacks \
                   --stack-name iamrole \
                   --profile personal \
                   --query "Stacks[0].Outputs[?OutputKey=='IamRole'].OutputValue" \
                   --output text)
aws sts assume-role --role-arn $IAM_ROLE_ARN \
                    --role-session-name tmp
```
We will use these short-term credentials to invoke creation of our Bucket stack
```bash
export AWS_ACCESS_KEY_ID=… 
export AWS_SECRET_ACCESS_KEY=…
export AWS_SESSION_TOKEN=…
aws cloudformation create-stack \
                   --stack-name mybucket \
                   --template-body file://MyBucket.yaml
```
We will see that our stack creation failed. Let's create a new role for CloudFormation
```bash
aws cloudformation create-stack \
                   --stack-name cfniamrole \
                   --capabilities CAPABILITY_IAM \
                   --template-body file://CfnIamRole.yaml
```
And use this role to create our stack.
```bash
IAM_ROLE_ARN=$(aws cloudformation describe-stacks \
                   --stack-name cfniamrole \
                   --query "Stacks[0].Outputs[?OutputKey=='IamRole'].OutputValue" \
                   --output text)
aws cloudformation create-stack \
                   --stack-name mybucket \
                   --template-body file://MyBucket.yaml \
                   --role-arn $IAM_ROLE_ARN
```
And validate that our bucket is created.
```bash
aws s3 ls
```
Don't forget to clean up your stacks:
```bash
for i in mybucket iamrole cfniamrole; do aws cloudformation delete-stack --stack-name $i ; done
```