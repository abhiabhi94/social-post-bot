import sys
from process_feed import process_feed
from social_posting.post_to_fb import fb_post
from social_posting.post_to_twitter import twitter_post
from social_posting.post_to_insta import insta_post
from social_posting.post_to_linkedin import linkedin_post
from social_posting.post_to_telegram import telegram_post

posts = process_feed()

if not posts:
    sys.exit('No new links found. Exiting')


def process_resposne(response):
    """
    Returns
        str: success if the resposne is boolean(expecting true)
        or the exception if it is not bool

    Params
        response: str
            The string returned from the function used for posting to social
            sites. 
    """
    return 'success' if type(response) == bool else response


resposne = []
for post in posts:
    response_fb = process_resposne(fb_post(post))
    response_twitter = process_resposne(twitter_post(post))
    # insta_post()
    # linkedin_post()
    response_telegram = process_resposne(telegram_post(post))

    resposne.append(f"""The response of posting the post:{post} on the social sites was:
    Facebook: {response_fb}  
    Twitter: {response_twitter}  
    Telegram: {response_telegram}  
    """
                    )
# Inform the admin about the posting
telegram_post(resposne, post_to_channel=False)
