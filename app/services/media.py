import boto3

from app.config import settings


session = boto3.Session(
    aws_access_key_id=settings.ZAWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.ZAWS_SECRET_ACCESS_KEY,
    region_name=settings.ZAWS_REGION_NAME
)

s3_client = session.client('s3', config=boto3.session.Config(
    signature_version='s3v4'
    ))


def generate_signed_url(object_name, format, expiration=3600):
    try:
        key_with_format = f"{object_name}.{format}"
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.ZAWS_S3_BUCKET_NAME,
                'Key': key_with_format,
                'ACL': 'public-read'
            },
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        return e
