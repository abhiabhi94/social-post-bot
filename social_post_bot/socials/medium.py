import json
import os
from typing import Union, ClassVar

import requests

from social_post_bot.feeds.processor import Message
from .base import BaseSocialSender


class Medium(BaseSocialSender):
    _api_url: ClassVar[str] = (
        f'https://api.medium.com/v1/users/{os.getenv("MEDIUM_USER_ID")}/posts'
    )
    _access_token: ClassVar[str] = os.getenv('MEDIUM_ACCESS_TOKEN', '')
    _content_format: ClassVar[str] = os.getenv('MEDIUM_FORMAT', 'html')
    _end_text: ClassVar[str] = os.getenv('MEDIUM_END_TXT', '')

    def __init__(self, post: Message) -> None:
        super().__init__(post)
        # this is required because as of the time of writing, medium wants this
        #  for the title to be displayed on the detail page
        self._add_title_to_content()
        self._add_end_text_to_content()

    def _add_title_to_content(self) -> None:
        self.post = self.post._replace(
            content=f'<h1>{self.post.title}</h1>' + self.post.content
        )

    def _add_end_text_to_content(self) -> None:
        self.post = self.post._replace(content=self.post.content + self._end_text)

    def send_post(self) -> Union[bool, str]:
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Charset": "utf-8"
        }

        data = {
            'content': self.post.content,
            'title': self.post.title,
            'canonicalUrl': self.post.link,
            'contentFormat': self._content_format,
            'tags': self.post.tags
        }
        try:
            response = requests.post(
                self._api_url, data=json.dumps(data), headers=headers)
            if response.status_code == 201:
                return True
            return response.text
        except Exception as exc:
            return (
                f'Exception occured during posting to Medium for {self.post.link}:'
                f' {exc}'
            )
