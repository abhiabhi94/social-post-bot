import sys
from typing import List, NamedTuple

import feedparser
from pymysql.cursors import Cursor
from pymysql.err import IntegrityError

from social_post_bot.db_connect import connect
from social_post_bot.logging_handler import logger

from .parser import parse_feed


class Message(NamedTuple):
    link: str
    text: str
    title: str
    content: str
    tags: List[str] = []


def process_feed() -> List[Message]:
    """
    Returns
        A list of messages with the links to be posted on different social platforms.
    """
    custom_txt, items = parse_feed()

    """Sample Post will be of the form:
        TITLE_OF_THE_POST
        https://LINK_TO_POST
    """

    def get_tags(item: feedparser.FeedParserDict) -> List[str]:
        if hasattr(item, 'tags'):
            return [t.term for t in item.tags]
        return []

    messages = []
    table, col, connection = connect()
    insertion_query = """INSERT INTO {} ({}) VALUES (%s) """.format(table, col)
    with connection:    # type: ignore
        for item in items:
            link: str = item.link
            with connection.cursor() as cursor:  # type:Cursor
                try:
                    cursor.execute(insertion_query, (link, ))
                    messages.append(
                        Message(
                            text=custom_txt,
                            title=item.title,
                            link=link,
                            content=item.description,
                            tags=get_tags(item)
                        )
                    )
                except IntegrityError:
                    logger.info(f'Duplicate link : {link}')
                    continue
        connection.commit()

    return messages


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    sys.stdout.write(f'{len(process_feed())} entries were added to the database.')
