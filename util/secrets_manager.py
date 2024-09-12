import logging

import boto3

logger = logging.getLogger(__name__)

def get_secret(secret_name, use_secrets_manager=True):
    """get values from Secrets Manager"""
    try:
        if use_secrets_manager:
            client = boto3.client('secretsmanager')
            response = client.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        else:
            client = boto3.client('ssm')
            response = client.get_parameter(Name=secret_name, WithDecryption=True)
            return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}", exc_info=True)
        return None
