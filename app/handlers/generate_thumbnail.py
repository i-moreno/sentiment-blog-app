import boto3
import io
import re

from PIL import Image
from app.repo.post import BlogRepository
from app.models.post import PostMediaUpdate

s3_client = boto3.client("s3")
blog_repo = BlogRepository()


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

            thumbnail_url = f"https://{bucket}.s3.amazonaws.com/{thumbnail_key}"
            print(f"Thumbnail created: {thumbnail_url}")

            # Extract post_id from the key using a regex.
            # Assuming key format: /images/{post_id}/{filename}
            match = re.match(r"images/([^/]+)/.*", key)
            if match:
                post_id = match.group(1)

                # Update DynamoDB record with thumbnail URL.
                post_media_update = PostMediaUpdate(
                    thumbnail_url=thumbnail_url)
                updated_post = blog_repo.update_post_media(
                    post_id, post_media_update)
                print(f"Updated post media, {updated_post}")
            else:
                print("Post ID could not be extracted from key; skipping DB update.")

        except Exception as e:
            print(f"Error processing {key} from bucket {bucket}: {e}")
