import boto3
import uuid


class S3Service:
    def __init__(self, bucket_name: str) -> None:
        self.client = boto3.client("s3")
        self.bucket = bucket_name

    def upload_image(self, filename: str, file_bytes: bytes, content_type: str, post_id: str) -> str:
        # Generate a unique key for the image
        file_key = f"images/{post_id}/{uuid.uuid4()}_{filename}"
        self.client.put_object(
            Bucket=self.bucket,
            Key=file_key,
            Body=file_bytes,
            ContentType=content_type
        )
        # Construct and return the image URL
        return f"https://{self.bucket}.s3.amazonaws.com/{file_key}"
