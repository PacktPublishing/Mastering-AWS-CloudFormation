# Template Macros

## AMI filler

Deploy Macro stack
```bash
aws cloudformation deploy --stack-name ami-filler-macro --template-file macro.yaml --capabilities CAPABILITY_IAM
```
Deploy Launch Template stack
```bash
aws cloudformation deploy --stack-name lt --template-file lt.yaml
```

## Standard App
Deploy Core stack
```bash
aws cloudformation deploy --stack-name core --template-file core.yaml --capabilities CAPABILITY_IAM
```
Create bucket and upload the code
```bash
aws s3 mb s3://masteringcfn
zip lambda-macro.zip standard-app.py
aws s3 cp lambda-macro.zip s3://masteringcfn
```
Deploy Macro stack
```bash
aws cloudformation deploy --stack-name standard-app-macro --template-file macro.yaml --capabilities CAPABILITY_IAM
```
Deploy Standard app stack
```bash
aws cloudformation deploy --stack-name app --template-file app.yaml
```