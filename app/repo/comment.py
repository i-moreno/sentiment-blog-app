import uuid

from app.db import table
from typing import Dict, Any
from app.models.comment import Comment
from datetime import datetime, timezone


class CommentRepository:
    def __init__(self):
        self.table = table

    def create_comment(self, post_id: str, comment: Comment) -> Dict[str, Any]:
        # Generate a unique comment_id
        if not comment.comment_id:
            comment.comment_id = str(uuid.uuid4())

        item = comment.model_dump()
        comment_creation_day = datetime.now(timezone.utc).isoformat()
        item["created_at"] = comment_creation_day
        item["archived"] = False

        # Primary keys
        item["PK"] = f"BLOG#{post_id}"
        item["SK"] = f"COMMENT#{comment.comment_id}"

        self.table.put_item(Item=item)
        return item

    def get_post_comments(self, post_id: str, limit=5, last_evaluated_pk=None, last_evaluated_sk=None):
        expression = {
            'KeyConditionExpression': 'PK = :pk AND begins_with(SK, :sk)',
            'ExpressionAttributeValues': {
                ':pk': f"BLOG#{post_id}",
                ':sk': 'COMMENT#'
            },
            'Limit': limit,
            'ScanIndexForward': True
        }

        # Exclude archived comments
        expression['FilterExpression'] = "attribute_not_exists(archived) OR archived = :false"
        expression['ExpressionAttributeValues'][':false'] = False

        if last_evaluated_pk:
            expression['ExclusiveStartKey'] = {
                "PK": last_evaluated_pk,
                "SK": last_evaluated_sk
            }

        response = self.table.query(**expression)
        items = response.get('Items', [])
        last_key = response.get('LastEvaluatedKey')
        return items, last_key

    def update_comment(self, post_id: str, comment_id: str, comment: Dict[str, str]):
        # Build UpdateExpression dynamically
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}

        comment = comment.model_dump(exclude_none=True)
        last_updated_at = datetime.now(timezone.utc).isoformat()
        comment['last_updated_at'] = last_updated_at

        for key, value in comment.items():
            # Map attribute names to avoid conflicts with reserved keywords
            attr_name = f"#{key}"
            attr_value = f":{key}"

            update_expression += f"{attr_name} = {attr_value}, "
            expression_attribute_values[attr_value] = value
            expression_attribute_names[attr_name] = key

        # Remove the trailing comma and space
        update_expression = update_expression.rstrip(", ")

        response = self.table.update_item(
            Key={
                'PK': f'BLOG#{post_id}',
                'SK': f'COMMENT#{comment_id}'
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"  # Return the updated comment
        )

        return response.get('Attributes', {})

    def delete_comment(self, post_id: str, comment_id: str) -> Dict[str, Any]:
        response = self.table.update_item(
            Key={
                'PK': f'BLOG#{post_id}',
                'SK': f'COMMENT#{comment_id}'
            },
            UpdateExpression="SET archived = :archived",
            ExpressionAttributeValues={
                ":archived": True
            },
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes', {})
