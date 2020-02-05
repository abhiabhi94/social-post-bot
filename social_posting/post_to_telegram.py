"""Post the text to a Telegram channel"""
import requests
from creds.read_creds import read_cred_file


CRED_FILE = 'telegram_creds.json'
API_URL = 'https://api.telegram.org/bot{}/sendMessage'


def notify_admin(token, admin, channel, text):
    """
    Notify the administrator about the last text posted in the channel
    Returns
        None

    Params
        token: str
            Access token for the telegram robot
        admin: str
            Id of the chat between the robot and the admin
        channel: str
            Id of the channel where the message was sent
        text: str
            The message that was posted in the channel
    """
    params = {
        'chat_id': admin,
        'text': f'In the channel @{channel}, this message was posted:\n{text}',
    }

    requests.post(API_URL.format(token), data=params)


def telegram_post(text, post_to_channel=True):
    """
    Returns
        bool : if the text was successfully posted
        OR
        str: a message along with the exception in case the post was unsuccessfull.

    Params
        text: str
            The complete text to be posted.
        post_to_channel: bool
            default: True
            Whether the text has to be posted to the channel or not.
    """

    creds = read_cred_file(CRED_FILE)
    try:
        token = creds['token']
        channel = creds['channel']

        params = {
            'chat_id': f'@{channel}',
            'text': text
        }

        if post_to_channel:
            requests.post(API_URL.format(token), data=params)
        notify_admin(token, creds['admin_id'], channel, text)

    except Exception as _:
        return f'Exception occured during posting to telegram: {_}'

    return True
