import logging
from datetime import datetime
from datetime import timedelta

import cloudscraper
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def scrape_chapters(url):
    """Scrape chapters from website"""
    scraper = cloudscraper.create_scraper(interpreter='nodejs', browser='chrome')

    try:
        response = scraper.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to retrieve, {response.status_code}, error: {response.text}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        chapters = soup.select('ul.chapter-list > li')
        chapter_list = []

        current_time = datetime.now()
        time_limit = current_time - timedelta(hours=48)

        for chapter in chapters:
            chapter_no = chapter.get('data-chapterno')
            chapter_title = chapter.select_one('strong.chapter-title').text.strip()
            chapter_time = chapter.select_one('time.chapter-update')['datetime']
            chapter_url = chapter.select_one('a')['href']

            chapter_time = datetime.strptime(chapter_time, '%Y-%m-%d %H:%M')

            if chapter_time < time_limit:
                logger.info(f"{chapter_no} is older than 48 hours, skipping...")
                continue

            chapter_data = {
                'chapter_no': str(chapter_no),
                'chapter_title': chapter_title,
                'chapter_url': chapter_url,
            }
            chapter_list.append(chapter_data)

        return chapter_list

    except Exception as e:
        logger.error(f"Error during scraping: {e}", exc_info=True)
        return []
