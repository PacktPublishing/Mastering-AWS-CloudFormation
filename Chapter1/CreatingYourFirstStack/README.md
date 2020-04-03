# Creating the stack

Make sure you are in this directory and run the following command.
> Note that if you have multiple profiles like me, you want to add --profile $PROFILE_NAME at the end of your command
```bash
aws cloudformation create-stack --stack-name mybucket --template-body file://MyBucket.yaml
```
You will see the `stackId` of your CloudFormation stack.
After a while your bucket will be created and you can verify it by running the following command
```bash
aws s3 ls
```

#Updating the stack

Run the following command to update your stack and add the PublicAccess to the bucket. Note that name of the template is now different.
```bash
aws cloudformation update-stack --stack-name mybucket --template-body file://MyBucket_with_public_read.yaml
```
You will receive the same `stackId` in the output.
You can review the status of the update operation by running `describe-stacks` command
```bash
aws cloudformation describe-stacks --stack-name mybucket
```
You should see the following line in your JSON response:
```json
{
    "Stacks": [
        {
            // ...
            "StackStatus": "UPDATE_COMPLETE"
            // ...
        }    
    ]
}
```
You can check if the changes were applied to your bucket by running the following:
```bash
aws s3api get-bucket-acl --bucket $YOUR_BUCKET_NAME
```
You will see the following block in the output:
```json
{
    "Grantee": {
        "Type": "Group",
        "URI": "http://acs.amazonaws.com/groups/global/AllUsers"
    },
    "Permission": "READ"
}
```