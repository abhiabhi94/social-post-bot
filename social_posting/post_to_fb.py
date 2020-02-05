"""Post the text to Facebook"""
import facebook
from creds.read_creds import read_cred_file


CRED_FILE = 'fb_creds.json'


def fb_post(text):
    """
    Returns
        bool : if the text was successfully posted
        OR
        str: a message along with the exception in case the post was unsuccessfull.

    Params
        text: str
            The complete text to be pasted.
    """
    creds = read_cred_file(CRED_FILE)
    try:
        graph = facebook.GraphAPI(access_token=creds['access_token'])
        graph.put_object(parent_object=creds['page_id'],
                         connection_name='feed',
                         message=text
                         )
    except Exception as _:
        return f'Exception occured during posting to facebook: {_}'

    return True
