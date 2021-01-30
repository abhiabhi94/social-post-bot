"""Post the text to Twitter"""
import os
from typing import Union, ClassVar

import twitter

from .base import BaseSocialSender


class Twitter(BaseSocialSender):
    _api:ClassVar = twitter.Api(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
            access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

    def send_post(self) -> Union[bool, str]:
        try:
            # Insert a new line in between
            self._api.PostUpdates('\n'.join(
                [self.post.text, self.post.title, self.post.link]
            ))
        except Exception as exc:
            return f'Exception occured during posting to Twitter: {exc}'

        return True
