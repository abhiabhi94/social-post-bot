"""Post the text to a Telegram channel"""
import requests
from creds.read_creds import read_cred_file


CRED_FILE = 'telegram_creds.json'
API_URL = 'https://api.telegram.org/bot{}/sendMessage?parse_mode=markdown'


def check_status(r):
    """
    Returns
        bool : if the post was successful
        str : if the post was unsuccessful

    Params:
        r: object
            response object received after the request.
    """
    if r.status_code == 200:
        return True
    else:
        return f'The post to Telegram failed with an error code:{r.raise_for_status}'


def notify_admin(token, admin, channel, text):
    """
    Notify the administrator about the last text posted in the channel
    Returns
        The resposne received from the request object after it's execution.

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
        'text': f'In the channel @{channel}, this message was posted: {text}',
    }

    try:
        response = requests.post(API_URL.format(token), data=params)
    except Exception as _:
        return f'Exception occured during posting to Telegram Admin: {_}'

    return check_status(response)


def telegram_post(title, link='', text='', post_to_channel=True):
    """
    Returns
        The response received from the request object after it's execution.

    Params
        title: str
            the title of the post
        link: str
            the link to be posted
        text: str
            the customary text to be posted on every post
        post_to_channel: bool
            Whether the text has to be posted to the channel or not.
    """
    creds = read_cred_file(CRED_FILE)
    try:
        token = creds['token']
        channel = creds['channel']

        # Insert two new lines in-between, make the title bold
        text_to_post = '\n\n'.join([text, f'*{title}*', link])

        params = {
            'chat_id': f'@{channel}',
            'text': text_to_post,
        }

        if post_to_channel:
            response = requests.post(API_URL.format(token), data=params)
            return check_status(response)

    except Exception as _:
        return f'Exception occured during posting to Telegram channel: {_}'

    return notify_admin(token,
                        creds['admin_id'],
                        channel,
                        text_to_post
                        )
