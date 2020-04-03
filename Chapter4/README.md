# Smoke tests

Create a "non working" ASG stack (use your own default VPC ID and Subnet IDs)
```bash
aws cloudformation deploy \
                     --template-file broken_asg.yaml \
                     --stack-name broken \
                     --parameter-overrides VpcId=vpc-12345678\
                     SubnetIds=subnet-123,subnet-456,subnet-789,subnet-012,subnet-345,subnet-678
```
Obtain ELB URL
```bash
aws cloudformation describe-stacks --stack-name broken | jq .[][].Outputs[].OutputValue
```
Run the test
```bash
python asg_test.py broken
```
Apply the "fix" on the stack
```bash
aws cloudformation deploy \
                     --template-file working_asg.yaml \
                     --stack-name broken \
                     --parameter-overrides VpcId=vpc-12345678\
                     SubnetIds=subnet-123,subnet-456,subnet-789,subnet-012,subnet-345,subnet-678
```
Run the test again

Create a "non compliant" Core stack
```bash
aws cloudformation deploy --stack-name core --template-file core_non_compliant.yaml --capabilities CAPABILITY_IAM
```
Run testing:
```bash
python core_subnets.py core
```
Deploy a fix:
```bash
aws cloudformation deploy --stack-name core --template-file core_compliant.yaml --capabilities CAPABILITY_IAM
```
Run the test again.

# Continuous Delivery

Deploy the CI/CD stack
```bash
aws cloudformation deploy \
                   --stack-name cicd \
                   --template-file cicd.yaml \
                   --capabilities CAPABILITY_IAM
```
From the AWS Console add all the necessary files to the repository. Add buildspec.yml last to avoid tmp stacks conflict.
If you had several failures (you definitely had) rerun the pipeline or retry it from the last failed stage.

