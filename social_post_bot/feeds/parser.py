"""Parse and Return Feed contents"""
import os
import sys
from typing import List, Tuple

import feedparser


def parse_feed() -> Tuple[str, List[feedparser.FeedParserDict]]:
    """
    Returns
        tuple:
            the customary message.
            the list of feed items.
    """
    feed = feedparser.parse(os.getenv('FEED_URL'))
    # By default the value will be a blank string
    custom_txt = os.getenv('CUSTOM_TXT', '')

    if feed['bozo']:
        sys.stdout.write((
            'The format of the feed does not seem to be correct.'
            ' Try making changes and parse again.'
            ))
        sys.exit(1)
    return custom_txt, feed['items']
