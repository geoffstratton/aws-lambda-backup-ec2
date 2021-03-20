import boto3

def lambda_handler(event, context):
    
    # Use Secure Token Service to get caller ID
    # Otherwise you'll get ALL public snapshots!
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
        for region in ec2_client.describe_regions()['Regions']]
        
    for region in regions:
        print("Instances in EC2 Region {0}:".format(region))
        ec2 = boto3.resource('ec2', region_name=region)
        
        response = ec2_client.describe_snapshots(OwnerIds=[account_id])
        snapshots = response["Snapshots"]
        
        # Sort snapshots by date, ascending
        snapshots.sort(key=lambda x: x['StartTime'])
        
        # Remove snapshots we want to keep (3 most recent)
        snapshots = snapshots[:-3]
        
        for snapshot in snapshots:
            id = snapshot['SnapshotId']
            try:
                print("Deleting snapshot: ", id)
                ec2_client.delete_snapshot(SnapshotId=id)
            except Exception as e:
                if "InvalidSnapshot.Inuse" in e.message:
                    print("Snapshot {} in use, skipping".format(id))
                    continue