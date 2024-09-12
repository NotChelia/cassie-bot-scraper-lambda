import logging
from datetime import datetime

import boto3

logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
notified_chapters_table = dynamodb.Table('notified-chapters')
scraper_url_table = dynamodb.Table('cassie-bot-scraper-url')

CHAPTER_URL_TEMPLATE = "https://www.lightnovelworld.co/novel/shadow-slave-1365/chapter-{chapter_no}"

def get_scrape_url(site):
    """Retrieve the URL to scrape for the site from DynamoDB"""
    try:
        response = scraper_url_table.get_item(Key={'site': site})
        if 'Item' in response:
            return response['Item']['url']
        else:
            logger.error(f"URL not found for site: {site}")
            return None
    except Exception as e:
        logger.error(f"Error retrieving URL from DynamoDB for site {site}: {e}", exc_info=True)
        return None

def is_chapter_notified(chapter_no):
    """Check if chapter has already been notified"""
    try:
        response = notified_chapters_table.get_item(Key={'chapter_no': int(chapter_no)})
        return 'Item' in response
    except Exception as e:
        logger.error(f"Error querying DynamoDB for chapter {chapter_no}: {e}", exc_info=True)
        return False

def mark_chapter_as_notified(chapter_no, chapter_data):
    """Mark chapter as notified"""
    try:
        chapter_url = CHAPTER_URL_TEMPLATE.format(chapter_no=chapter_no)

        notified_chapters_table.put_item(
            Item={
                'chapter_no': int(chapter_no),
                'chapter_title': chapter_data['chapter_title'],
                'chapter_url': chapter_url,
                'notified_at': datetime.now().isoformat()
            }
        )
        logger.info(f"Chapter {chapter_no} marked as notified")
    except Exception as e:
        logger.error(f"Error updating DynamoDB for chapter {chapter_no}: {e}", exc_info=True)
