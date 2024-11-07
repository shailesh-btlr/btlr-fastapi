import boto3
from app.config import settings


def send_otp_email(otp, recipient_email):
    subject = f"OTP : {otp}"
    body = f"Your OTP is: {otp}"
    ses_client = boto3.client("ses", region_name=settings.ZAWS_REGION_NAME)
    ses_client.send_email(
        Source=settings.OTP_EMAIL_FROM_ADDRESS,
        Destination={
            "ToAddresses": [
                recipient_email,
            ]
        },
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
    )
