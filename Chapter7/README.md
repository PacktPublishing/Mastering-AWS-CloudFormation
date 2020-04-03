# Custom resources

Package lambda and store it on S3
```bash
cd custom-db
pip install -t . -r requirements.txt --upgrade
aws s3 mb s3://masteringcloudformation
zip -r lambda-cr.zip *
aws s3 cp lambda-cr.zip s3://masteringcloudformation
```

Create CR and RDS stack
```bash
cd ..
aws cloudformation deploy --stack-name cr --template-file cr.yaml --capabilities CAPABILITY_IAM
aws cloudformation deploy --template-file rds.yaml --stack-name rds --parameter-overrides VpcId=$VPC
```

Create your custom resource
```bash
aws cloudformation deploy --stack-name customdb --template-file customdb.yaml
```

Test "broken" custom resource
```bash
aws cloudformation deploy --stack-name customdb-broken --template-file customdb_missing_property.yaml
```