"""Post the text to Twitter"""
import twitter
from creds.read_creds import read_cred_file

CRED_FILE = 'twitter_creds.json'


def twitter_post(text, link):
    """
    Returns
        bool : if the text was successfully posted
        OR
        str: a message along with the exception in case the post was unsuccessfull.

    Params
        text: str
            the text to be posted
        link: str
            the link to be posted
    """
    cred = read_cred_file(CRED_FILE)

    try:
        api = twitter.Api(
            consumer_key=cred['api_key'],
            consumer_secret=cred['api_secret_key'],
            access_token_key=cred['access_token_key'],
            access_token_secret=cred['access_token_secret']
        )
        tweet = api.PostUpdates('\n'.join([text, link]))
    except Exception as _:
        return f'Exception occured during posting to twitter: {_}'

    return True
