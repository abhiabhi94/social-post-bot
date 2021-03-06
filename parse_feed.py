"""Parse and Return Feed contents"""
import sys
import feedparser
from creds.read_creds import read_cred_file

CRED_FILE = 'feed_creds.json'


def parse_feed():
    """
    Returns
        tuple:
            the customary message.
            the list of feed items.
    """
    creds = read_cred_file(CRED_FILE)
    feed = feedparser.parse(creds['URL'])
    # By default the value will be a blank string
    custom_txt = dict.get(creds, 'CUSTOM_TXT', '')

    if feed['bozo']:
        sys.exit(
            'The format of the feed does not seem to be correct. Try making changes and parse again.')
    return custom_txt, feed['items']
