"""Post the text to LinkedIn"""
import requests
from creds.read_creds import read_cred_file


CRED_FILE = 'linkedin_creds.json'
API_URL = 'https://api.linkedin.com/v2/shares'


def linkedin_post(text, link):
    """
    Returns
        bool : if the text was successfully posted
        OR
        str: a message along with the exception in case the post was unsuccessfull.

    Params
        text: str
            the text to be posted
        link: str
            default: ''
            the link to be posted
    """
    creds = read_cred_file(CRED_FILE)

    params = {
        'text': text,
        'owner': creds['client_id'],
    }
