"""Parse and Return Feed contents"""
import sys
import feedparser
from creds.read_creds import read_cred_file

CRED_FILE = 'feed_creds.json'


def parse_feed():
    """
    Returns
        the list of feed items.
    """
    creds = read_cred_file(CRED_FILE)
    feed = feedparser.parse(creds['URL'])

    if feed['bozo']:
        sys.exit(
            'The format of the feed does not seem to be correct. Try making changes and parse again.')
    return feed['items']
