import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Step 1: Get all snapshots created by your account
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    
    # Step 2: Get all running EC2 instances
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    # Collect all volume IDs from running instances
    attached_volumes = set()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for block_device in instance.get("BlockDeviceMappings", []):
                if 'Ebs' in block_device:
                    attached_volumes.add(block_device['Ebs']['VolumeId'])

    # Step 3: Find snapshots not belonging to these attached volumes
    unused_snapshots = []
    for snap in snapshots:
        if snap['VolumeId'] not in attached_volumes:
            unused_snapshots.append(snap['SnapshotId'])

    # Step 4: Delete unused snapshots
    for snap_id in unused_snapshots:
        try:
            print(f"Deleting unused snapshot: {snap_id}")
            ec2.delete_snapshot(SnapshotId=snap_id)
        except Exception as e:
            print(f"Error deleting {snap_id}: {e}")

    return {
        'statusCode': 200,
        'body': f"Deleted {len(unused_snapshots)} unused snapshots"
    }
