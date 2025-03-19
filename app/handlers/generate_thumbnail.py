import boto3
import io
from PIL import Image

s3_client = boto3.client("s3")


def generate_thumbnail(event, context):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Skip if this is already a thumbnail
        if key.startswith("thumbnails/"):
            continue

        try:
            # Download the image
            response = s3_client.get_object(Bucket=bucket, Key=key)
            image_content = response["Body"].read()

            # Open image and create thumbnail
            image = Image.open(io.BytesIO(image_content))
            thumbnail_size = (300, 300)  # adjust as needed
            image.thumbnail(thumbnail_size)

            # Save thumbnail to buffer
            buffer = io.BytesIO()
            image_format = image.format if image.format else "JPEG"
            image.save(buffer, image_format)
            buffer.seek(0)

            # Define thumbnail key
            thumbnail_key = f"thumbnails/{key}"

            # Upload thumbnail to S3
            s3_client.put_object(
                Bucket=bucket,
                Key=thumbnail_key,
                Body=buffer,
                ContentType=response["ContentType"]
            )

            print(f"Thumbnail created: {thumbnail_key}")

        except Exception as e:
            print(f"Error processing {key} from bucket {bucket}: {e}")
