import uuid

from app.db import table
from typing import Dict, Any
from app.models.post import BlogPost, PostMediaUpdate
from datetime import datetime, timezone


class BlogRepository:
    def __init__(self):
        self.table = table

    def create_post(self, post: BlogPost) -> Dict[str, Any]:
        # Generate a unique post_id if not provided
        if not post.post_id:
            post.post_id = str(uuid.uuid4())

        item = post.model_dump()
        post_creation_day = datetime.now(timezone.utc).isoformat()
        item["created_at"] = post_creation_day

        # Primary keys
        item["PK"] = f"BLOG#{post.post_id}"
        item["SK"] = "META"
        # Add additional attributes for the GSI
        item["GSI1PK"] = "BLOG"
        item["GSI1SK"] = post_creation_day

        self.table.put_item(Item=item)
        return item

    def read_posts(self, limit=10, last_evaluated_pk=None, last_evaluated_gsi: str = None, sort_order='DESC'):
        """
        Read (list) all blog posts by querying the GSI.
        This assumes that every post is indexed with:
        - GSI1PK = "BLOG"
        - GSI1SK = <some sortable attribute like created_at>
        """
        expression = {
            'TableName': 'BlogAppTable',  # TODO: Parametrize this
            'IndexName': 'GSI1',
            'KeyConditionExpression': 'GSI1PK = :pk',
            'ExpressionAttributeValues': {':pk': 'BLOG'},
            'Limit': limit,
            'ScanIndexForward': True if sort_order == 'ASC' else False,
        }

        # Filter by archived status
        expression['FilterExpression'] = "attribute_not_exists(archived) OR archived = :false"
        expression['ExpressionAttributeValues'][':false'] = False

        if last_evaluated_pk and last_evaluated_gsi:
            expression['ExclusiveStartKey'] = {
                "PK": last_evaluated_pk,
                "SK": "META",
                "GSI1PK": "BLOG",
                "GSI1SK": last_evaluated_gsi
            }

        try:
            response = self.table.query(**expression)
            items = response.get('Items', [])
            last_key = response.get('LastEvaluatedKey')
            return items, last_key

        except ValueError as e:
            raise ValueError(
                f"DynamoDB query failed: {e.response['Error']['Message']}")

    def update_post_media(self, post_id: str, media: PostMediaUpdate) -> Dict[str, Any]:
        key = {
            "PK": f"BLOG#{post_id}",
            "SK": "META"
        }

        # Convert the model to a dictionary
        media_dict = media.model_dump(exclude_none=True)

        # Build the update expression and attribute values dynamically
        update_parts = []
        expression_attribute_values = {}
        for field, value in media_dict.items():
            update_parts.append(f"{field} = :{field}")
            expression_attribute_values[f":{field}"] = value

        update_expression = "SET " + ", ".join(update_parts)

        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        return response.get("Attributes")

    def update_post(self, post_id: str, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing blog post.

        Args:
            post_id (str): ID of the post to update.
            updates (Dict[str, Any]): Fields to update.

        Returns:
            Dict[str, Any]: Updated post.
        """

        # Build UpdateExpression dynamically
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}

        post = post.model_dump(exclude_none=True)
        last_updated_at = datetime.now(timezone.utc).isoformat()
        post['last_updated_at'] = last_updated_at

        for key, value in post.items():
            # Map attribute names to avoid conflicts with reserved keywords
            attr_name = f"#{key}"
            attr_value = f":{key}"

            update_expression += f"{attr_name} = {attr_value}, "
            expression_attribute_values[attr_value] = value
            expression_attribute_names[attr_name] = key

        # Remove the trailing comma and space
        update_expression = update_expression.rstrip(", ")

        try:
            response = self.table.update_item(
                Key={
                    'PK': f'BLOG#{post_id}',
                    'SK': 'META'
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"  # Return the updated post
            )

            return response.get('Attributes', {})
        except Exception as e:
            raise ValueError(f"Failed to update post {post_id}: {str(e)}")

    def delete_post(self, post_id: str) -> Dict[str, Any]:
        try:
            response = self.table.update_item(
                Key={
                    'PK': f'BLOG#{post_id}',
                    'SK': 'META'
                },
                UpdateExpression="SET archived = :archived",
                ExpressionAttributeValues={
                    ":archived": True
                },
                ReturnValues="ALL_NEW"
            )
            return response.get('Attributes', {})
        except Exception as e:
            raise ValueError(f"Failed to delete post {post_id}: {str(e)}")

    def restore_post(self, post_id: str) -> Dict[str, Any]:
        try:
            response = self.table.update_item(
                Key={
                    'PK': f'BLOG#{post_id}',
                    'SK': 'META'
                },
                UpdateExpression="SET archived = :archived",
                ExpressionAttributeValues={
                    ":archived": False
                },
                ReturnValues="ALL_NEW"
            )
            return response.get('Attributes', {})
        except Exception as e:
            raise ValueError(f"Failed to restore post {post_id}: {str(e)}")
