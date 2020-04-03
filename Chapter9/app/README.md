# CDK

## Preparation
Create virtualenv and install dependencies
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run tests
```bash
PYTHONPATH=. python tests/test_app.py -v
```

## Deploy all stacks
```bash
cdk deploy rds
```