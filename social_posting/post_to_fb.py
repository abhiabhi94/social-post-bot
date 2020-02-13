"""Post the text to Facebook"""
import facebook
from creds.read_creds import read_cred_file


CRED_FILE = 'fb_creds.json'


def fb_post(title, link, text=''):
    """
    Returns
        bool : if the text was successfully posted
        OR
        str: a message along with the exception in case the post was unsuccessfull.

    Params
        title: str
            the title of the post
        link: str
            the link to be posted
        text: str
            the customary text to be posted on every post
    """
    creds = read_cred_file(CRED_FILE)
    try:
        graph = facebook.GraphAPI(access_token=creds['access_token'])
        # Insert new line between the text and the title
        status = '\n'.join([text, title])
        graph.put_object(parent_object=creds['page_id'],
                         connection_name='feed',
                         message=status,
                         link=link,
                         )
    except Exception as _:
        return f'Exception occured during posting to facebook: {_}'

    return True
