# Multi-region

Deploy permissions stack
```bash
aws cloudformation deploy --stack-name ss-perm --template-file multi-region/StackSetPermissions.yaml --capabilities CAPABILITY_NAMED_IAM 
```
Create StackSet
```bash
aws cloudformation create-stack-set --stack-set-name core --template-body file://multi-region/core.yaml --capabilities CAPABILITY_NAMED_IAM 
```
Create Stack instances
```bash
aws cloudformation create-stack-instances --stack-set-name core --accounts ACCT_ID --regions eu-west-1 --parameter-overrides ParameterKey=VpcCidr,ParameterValue=10.1.0.0/16 ParameterKey=Environment,ParameterValue=test
aws cloudformation create-stack-instances --stack-set-name core --accounts ACCT_ID --regions us-east-1 --parameter-overrides ParameterKey=VpcCidr,ParameterValue=10.0.0.0/16 ParameterKey=Environment,ParameterValue=prod
```

# Multi-account

Deploy permission stacks to admin and target accounts
```bash
aws cloudformation deploy --stack-name Admin-Role --template-file multi-account/StackSetAdmin.yaml --capabilities CAPABILITY_NAMED_IAM
aws cloudformation deploy --stack-name Exec-Role --profile test --template-file multi-account/StackSetExec.yaml --parameter-overrides AdministratorAccountId=ACCT_ID --capabilities CAPABILITY_NAMED_IAM
aws cloudformation deploy --stack-name Exec-Role --profile prod --template-file multi-account/StackSetExec.yaml --parameter-overrides AdministratorAccountId=ACCT_ID --capabilities CAPABILITY_NAMED_IAM 
```

Create StackSet
```bash
aws cloudformation create-stack-set --stack-set-name core --template-body file://multi-account/core.yaml --capabilities CAPABILITY_NAMED_IAM 
```
Create Stack instances
```bash
aws cloudformation create-stack-instances --stack-set-name core --accounts ACCT_ID_PROD ACCT_ID_TEST --regions REGION --operation-preferences MaxConcurrentPercentage=100 
```

# TAG
Deploy permissions stack
```bash
aws cloudformation deploy --stack-name ss-perm --template-file multi-region/StackSetPermissions.yaml --capabilities CAPABILITY_NAMED_IAM 
```
Deploy TAG
```bash
aws cloudformation deploy --stack-name tag --template-file target-account-gate/tag.yaml --capabilities CAPABILITY_IAM 
```
Create StackSet and instances
```bash
aws cloudformation create-stack-set --stack-set-name webtier --template-body file://target-account-gate/webtier.yaml
aws cloudformation create-stack-instances --stack-set-name webtier --accounts ACCT_ID --regions eu-central-1 
```