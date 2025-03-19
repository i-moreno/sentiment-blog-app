import uuid

from app.db import table
from typing import Dict, Any
from app.models.sentiment import Sentiment
from datetime import datetime, timezone


class SentimentRepository:
    def __init__(self):
        self.table = table

    def create_sentiment(self, post_id: str, sentiment: Sentiment):
        sentiment_id = str(uuid.uuid4())
        sentiment_creation_day = datetime.now(timezone.utc).isoformat()

        item = sentiment.model_dump()
        item["sentiment_id"] = sentiment_id
        item["created_at"] = sentiment_creation_day
        item["PK"] = f"BLOG#{post_id}"
        item["SK"] = f"SENTIMENT#{sentiment_id}"

        self.table.put_item(Item=item)
        return item

    def update_sentiment(self, post_id: str,  sentiment_id: str, sentiment: Dict[str, str]):
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}

        sentiment = sentiment.model_dump(exclude_none=True)
        sentiment["last_updated_at"] = datetime.now(timezone.utc).isoformat()

        for key, value in sentiment.items():
            attr_name = f"#{key}"
            attr_value = f":{key}"
            update_expression += f"{attr_name} = {attr_value}, "
            expression_attribute_values[attr_value] = value
            expression_attribute_names[attr_name] = key

        # Remove the trailing comma and space
        update_expression = update_expression.rstrip(", ")

        response = self.table.update_item(
            Key={
                'PK': f"BLOG#{post_id}",
                'SK': f"SENTIMENT#{sentiment_id}"
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        return response.get('Attributes', {})
