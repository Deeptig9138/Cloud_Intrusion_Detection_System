In any and all cases to discuss about the project, changes in the project : www.linkedin.com/in/deepti-gupta-775736289

# Cloud Intrusion Detection System
Overview:
This system leverages machine learning and rule-based techniques to provide a robust solution for detecting potential security threats in AWS CloudTrail logs. The main components of the system include:
Log Collection: Fetches recent CloudTrail logs to monitor AWS activities.
Anomaly Detection: Uses the Isolation Forest algorithm to identify unusual API call patterns.
S3 Bucket Monitoring: Detects changes in S3 bucket permissions, specifically identifying if a bucket becomes public.
Alert System: Sends automated email alerts when potential security issues are detected.

## Requirements

- Python 3.x
- AWS account with CloudTrail logs
- Gmail account for sending alert emails

## Setup

```bash
git clone https://github.com/Deeptig9138/cloud-intrusion-detection.git
cd cloud-intrusion-detection

pip install -r requirements.txt

cp .env.example .env

