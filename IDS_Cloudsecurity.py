import os
import boto3
import numpy as np
from sklearn.ensemble import IsolationForest
import json
import smtplib
from email.mime.text import MIMEText
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS setup - environment variables for credentials
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
cloudtrail = session.client('cloudtrail')

# Email credentials from environment variables
sender_email = os.getenv('SENDER_EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')

def get_cloudtrail_logs():
    """Fetch the most recent CloudTrail logs"""
    try:
        response = cloudtrail.lookup_events(MaxResults=10)  # Fetch up to 10 recent events
        events = response['Events']
    except Exception as e:
        logger.error(f"Failed to fetch CloudTrail logs: {e}")
        events = []
    return events

def extract_api_call_counts(logs):
    """Extract API call counts from logs"""
    api_call_count_map = {}
    for log in logs:
        api_name = log.get('EventName', 'unknown')
        api_call_count_map[api_name] = api_call_count_map.get(api_name, 0) + 1
    return np.array(list(api_call_count_map.values())).reshape(-1, 1)

def detect_public_s3_buckets(logs):
    """Detect if an S3 bucket becomes public"""
    alerts = []
    for log in logs:
        if 'S3BucketPublicAccess' in log.get('EventName', ''):
            bucket_name = log.get('Resources', [{}])[0].get('ResourceName', 'unknown')
            alert_message = f"Alert: S3 Bucket {bucket_name} became public!"
            alerts.append(alert_message)
            logger.info(alert_message)
    return alerts

def detect_api_anomalies(logs):
    """Detect API call frequency anomalies using Isolation Forest"""
    api_call_counts = extract_api_call_counts(logs)

    if api_call_counts.size == 0:
        logger.info("No API call counts available for anomaly detection.")
        return []

    model = IsolationForest(contamination=0.1)
    model.fit(api_call_counts)
    predictions = model.predict(api_call_counts)

    anomaly_alerts = []
    for i, prediction in enumerate(predictions):
        if prediction == -1:  # -1 indicates an anomaly
            anomaly_message = f"Anomaly detected at index {i}, API call count: {api_call_counts[i][0]}"
            anomaly_alerts.append(anomaly_message)
            logger.info(anomaly_message)
    return anomaly_alerts

def send_alert_email(subject, body):
    """Send an email alert to the admin"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = os.getenv('RECEIVER_EMAIL')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, email_password)
            smtp_server.sendmail(sender_email, os.getenv('RECEIVER_EMAIL'), msg.as_string())
        logger.info("Alert email sent!")
    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")

def run_intrusion_detection():
    """Run the intrusion detection system"""
    # Step 1: Fetch CloudTrail logs
    logs = get_cloudtrail_logs()

    # Step 2: Run Rule-based Detection (S3 public access detection)
    rule_based_alerts = detect_public_s3_buckets(logs)

    # Step 3: Run Anomaly Detection (API anomaly detection)
    anomaly_alerts = detect_api_anomalies(logs)

    # Step 4: Send Alerts if necessary
    all_alerts = rule_based_alerts + anomaly_alerts
    if all_alerts:
        alert_body = "\n".join(all_alerts)
        send_alert_email("Cloud Intrusion Detection Alert", alert_body)
    else:
        logger.info("No alerts generated. System is normal.")

# Run the IDS system
if __name__ == "__main__":
    run_intrusion_detection()

