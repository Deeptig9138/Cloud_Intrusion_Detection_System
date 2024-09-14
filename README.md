In cases of discussion and changes, contact : www.linkedin.com/in/deepti-gupta-775736289

# Cloud Intrusion Detection System
Overview:
This system leverages machine learning and rule-based techniques to provide a robust solution for detecting potential security threats in AWS CloudTrail logs. The main components of the system include:
1) Log Collection: Fetches recent CloudTrail logs to monitor AWS activities.
2) Anomaly Detection: Uses the Isolation Forest algorithm to identify unusual API call patterns.
3) S3 Bucket Monitoring: Detects changes in S3 bucket permissions, specifically identifying if a bucket becomes public.
4) Alert System: Sends automated email alerts when potential security issues are detected.

Features:
1) Real-time Monitoring: Quickly detects and responds to potential security threats.
2) Advanced Analytics: Employs machine learning to detect anomalies.
3) Customizable Alerts: Configurable alerts to provide relevant information for timely responses.
4) Robust Logging: Detailed logging for better tracking and debugging.

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

