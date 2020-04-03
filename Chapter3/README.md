# Validation, linting and deployment of the stack
`Since I have multiple AWS profiles, I will append my commands with --profile argument`
## Validation
Validating broken template
```bash
aws cloudformation validate-template --template-body file://core_broken.yaml
```

Validating valid template
```bash
aws cloudformation validate-template --template-body file://core_full.yaml
```

## Linting
Running linter against broken template
```bash
cfn-lint core_broken.yaml
```
Running linter against all regions
```bash
cfn-lint core_full.yaml --regions 'ALL_REGIONS'
```
Running linter with custom rules
```bash
cfn-lint database_failing.yaml -a custom_rules
```

## Provisioning
Using `create-stack` and `update-stack`
```bash
aws cloudformation create-stack --stack-name core --template-body file://core_partial.yaml --parameters file://testing.json
aws cloudformation update-stack --stack-name core --template-body file://core_full.yaml --parameters file://testing.json --capabilities CAPABILITY_IAM
```

Using change sets
```bash
aws cloudformation create-stack --stack-name core --template-body file://core_partial.yaml --parameters file://testing.json
aws cloudformation create-change-set --stack-name core --change-set-name our-change-set --template-body file://core_full.yaml --parameters file://testing.json --capabilities CAPABILITY_IAM
aws cloudformation execute-change-set --change-set-name our-change-set --stack-name core
```
Using `deploy`
```bash
aws cloudformation deploy --stack-name core --template-file core_partial.yaml --capabilities CAPABILITY_IAM --parameter-overrides VpcCidr="10.1.0.0/16" Environment="test"
aws cloudformation deploy --stack-name core --template-file core_full.yaml --capabilities CAPABILITY_IAM --parameter-overrides VpcCidr="10.1.0.0/16" Environment="test"
```

## Drifts
Deploy the stack (if haven't before)
```bash
aws cloudformation deploy --template-file core_full.yaml --stack-name core --parameter-overrides VpcCidr=10.1.0.0/16 Environment=test --capabilities CAPABILITY_IAM
```
Obtain IAM Role name
```bash
aws cloudformation describe-stack-resource --stack-name core --logical-resource-id DevRole
```
Attach extra policy
```bash
aws iam attach-role-policy --role-name ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
```
Check the drift
```bash
aws cloudformation detect-stack-resource-drift --stack-name core --logical-resource-id DevRole
```
Apply the managed change
```bash
aws cloudformation deploy --template-file core_drift.yaml --stack-name core --parameter-overrides VpcCidr=10.1.0.0/16 Environment=test --capabilities CAPABILITY_IAM
```