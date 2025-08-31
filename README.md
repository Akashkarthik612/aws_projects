AWS Lambda – EC2 Unused Snapshot Cleaner

This AWS Lambda function helps in automated cloud optimization by identifying and removing unused EBS snapshots in your AWS account.

📌 Overview

Fetches all running EC2 instances and their attached volumes.

Compares them against all snapshots owned by your account.

Identifies snapshots not linked to any currently attached EBS volume.

Deletes those unused snapshots automatically.

Designed to be triggered by Amazon CloudWatch / EventBridge on a schedule (e.g., daily).

🚀 Benefits

Frees up storage costs by deleting unnecessary snapshots.

Improves cloud resource optimization.

Fully automated – no manual cleanup required.

⚙️ How It Works

The Lambda script calls AWS EC2 APIs using boto3.

Collects a list of all running EC2 volumes.

Collects all snapshots owned by your account.

Compares them and deletes snapshots not associated with active volumes.

🛠️ Setup

Deploy the Python script as a Lambda function.
Assign IAM Role with these permissions:
ec2:DescribeInstances
ec2:DescribeSnapshots
ec2:DeleteSnapshot
Create a CloudWatch Event Rule (EventBridge) to trigger the Lambda.



Test first in print-only mode before enabling deletion.

You may want to keep important snapshots – consider adding tag checks before deletion.
