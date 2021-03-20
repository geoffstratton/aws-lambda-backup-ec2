Repo Name
=========
aws-lambda-backup-ec2

Description
---------------
These are AWS Lambda functions for creating snapshots of EC2 instances, and pruning the backups to keep only x snapshots, using Python (tested with 3.7), Amazon's boto3 SDK, and some method of invoking the Lambda functions at specified times (e.g., a CloudWatch cron job).

Prerequisites
---------------
* The [boto3 SDK](https://aws.amazon.com/sdk-for-python/).
* Ensure that the IAM Role attached to the Lambda function has a policy with EC2. If you want to create a custom policy, include:
   + ec2:DescribeInstances
   + ec2:DeleteSnapshot
   + ec2:ModifySnapshotAttribute
   + ec2:CreateTags
   + ec2:DescribeRegions
   + ec2:ResetSnapshotAttribute
   + ec2:DescribeVolumes
   + ec2:CreateSnapshot
   + ec2:DescribeSnapshots
* Use the usual CloudWatch Logs role for logging.
* A cron job in CloudWatch to invoke the Lambda function at the desired times.
* Ensure that your EC2 instances to be backed up have a tag like "backup=True". You can of course modify the script to look for a different parameter. 

### Lambda logs
If the backups are working, you'll see entries like this in your Lambda log output: 

```
Backup of i-0354c71ccb445c242, volume vol-0ff3cdfcdc3264f68, created 2019-11-06T21:05:03
Created snapshot: snap-08998bb7426a12ef5
Backup of i-03ae177c787e0c955, volume vol-0517cc4c47979c61b, created 2019-11-06T21:05:03
Created snapshot: snap-09a8bfc3da4352339
```

### To set up boto3 for development (Amazon Linux and similar):
```
sudo yum install -y python3 python3-pip python3-setuptools
pip3 install boto3 --user
aws configure [enter your AWS access key and secret key]

python3
>>> import boto3
>>> ec2 = boto3.client('ec2')
>>> response = ec2.run_instances(ImageId='ami-00dc79254d0461090',InstanceType='t2.micro',KeyName='MY KEY',MinCount=1,MaxCount=1)
```

