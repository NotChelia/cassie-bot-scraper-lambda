import json

from app.chapter_scraper import scrape_chapters
from app.dynamo_handler import get_scrape_url
from app.dynamo_handler import is_chapter_notified
from app.dynamo_handler import mark_chapter_as_notified
from app.sqs_handler import publish_to_sqs
from util.logger_setup import setup_logging

logger = setup_logging()

def lambda_handler(event, context):
    logger.info("Lambda handler invoked")
    site = event.get('site', 'Shadow Slave')
    url = get_scrape_url(site)

    if not url:
        logger.error(f"URL not found for site: {site}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"URL not found for site: {site}")
        }

    chapters = scrape_chapters(url)

    for chapter in chapters:
        chapter_no = chapter['chapter_no']

        if not is_chapter_notified(chapter_no):
            message_id = publish_to_sqs(chapter)
            if message_id:
                mark_chapter_as_notified(chapter_no, chapter)
        else:
            logger.info(f"Chapter {chapter_no} already notified, skipping")

    return {
        'statusCode': 200,
        'body': json.dumps(f"{len(chapters)} chapters processed for {site}.")
    }

lambda_handler({}, {})
