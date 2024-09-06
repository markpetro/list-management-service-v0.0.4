import requests
import os
import logging

class NotificationService:
    def __init__(self):
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.email_service_url = os.getenv('EMAIL_SERVICE_URL')  # Example for email service
        self.sms_service_url = os.getenv('SMS_SERVICE_URL')  # Example for SMS service

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def send_slack_notification(self, message):
        if not self.webhook_url:
            self.logger.error("Slack webhook URL not configured.")
            return {"error": "Slack webhook URL not configured."}

        payload = {"text": message}
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            self.logger.info(f"Slack notification sent: {message}")
            return {"status": "Slack notification sent successfully"}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
            return {"error": f"Failed to send Slack notification: {e}"}

    def send_email_notification(self, to_email, subject, body):
        if not self.email_service_url:
            self.logger.error("Email service URL not configured.")
            return {"error": "Email service URL not configured."}

        payload = {"to": to_email, "subject": subject, "body": body}
        try:
            response = requests.post(self.email_service_url, json=payload)
            response.raise_for_status()
            self.logger.info(f"Email notification sent to {to_email}: {subject}")
            return {"status": "Email notification sent successfully"}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send email notification: {e}")
            return {"error": f"Failed to send email notification: {e}"}

    def send_sms_notification(self, phone_number, message):
        if not self.sms_service_url:
            self.logger.error("SMS service URL not configured.")
            return {"error": "SMS service URL not configured."}

        payload = {"to": phone_number, "message": message}
        try:
            response = requests.post(self.sms_service_url, json=payload)
            response.raise_for_status()
            self.logger.info(f"SMS notification sent to {phone_number}: {message}")
            return {"status": "SMS notification sent successfully"}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send SMS notification: {e}")
            return {"error": f"Failed to send SMS notification: {e}"}