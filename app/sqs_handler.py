import json
import logging

import boto3

from util.secrets_manager import get_secret

logger = logging.getLogger(__name__)

sqs = boto3.client('sqs', region_name='us-east-2')

def publish_to_sqs(chapter_data):
    """Publish chapter data to AWS SQS"""
    try:
        queue_url = get_secret('scraper_queue_url')

        if not queue_url:
            raise ValueError("SQS queue URL not found in SM")

        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(chapter_data)
        )
        return response['MessageId']
    except Exception as e:
        logger.error(f"Error publishing to SQS: {e}", exc_info=True)
        return None
