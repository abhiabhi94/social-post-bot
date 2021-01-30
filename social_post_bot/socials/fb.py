"""Post the text to Facebook"""
import os
from typing import Union, ClassVar

import facebook

from .base import BaseSocialSender


class Facebook(BaseSocialSender):
    _access_token: ClassVar[str] = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    _page_id: ClassVar[str] = os.getenv('FACEBOOK_PAGE_ID', '')

    def send_post(self) -> Union[bool, str]:
        try:
            graph = facebook.GraphAPI(access_token=self._access_token)
            # Insert new line between the text and the title
            status = '\n'.join([self.post.text, self.post.title])

            graph.put_object(
                parent_object=self._page_id,
                connection_name='feed',
                message=status,
                link=self.post.link,
                )
        except Exception as exc:
            return (
                f'Exception occured during posting to facebook for {self.post.link}:'
                f' {exc}'
            )

        return True
