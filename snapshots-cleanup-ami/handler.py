#
# A lambda function to check if the source AMIs of the
# Create by Image Snapshots are still existing.
# If the snapshots are already orphaned, it will be deleted.
#
# Created by : Mary Rose Quito
#
#

import boto3

def cleanupSnapshotsAmi(event, context):
    client = boto3.client('ec2', region_name="us-west-2")
    snapshotAll = client.describe_snapshots(
     OwnerIds=[
       'self',
     ],
     Filters=[
        {
            'Name':'description',
            'Values':[
                'Created by CreateImage*'
                ]
        }
     ]
    )['Snapshots']

    for snapshotId in snapshotAll:
        desc = snapshotId["Description"]
        ssId = snapshotId['SnapshotId']
        fields = desc.split(' ')
        #print(fields[4])

        imagesAll = client.describe_images(
         Owners=[
           'self',
         ],
         ImageIds=[
          fields[4],
         ],
        )['Images']

        if not imagesAll:
            print("Deleting orphaned snapshots")
            deleteSnapshot = client.delete_snapshot(
                SnapshotId=ssId
            )
