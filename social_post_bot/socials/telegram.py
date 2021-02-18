"""Post the text to a Telegram"""
import os
from typing import ClassVar, Dict, Union

import requests

from social_post_bot.logging_handler import logger

from .base import BaseSocialSender


class Telegram(BaseSocialSender):
    _api_url: ClassVar[str] = (
            f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/'
            'sendMessage?parse_mode=markdown'
        )
    _channel: ClassVar[str] = os.getenv('TELEGRAM_CHANNEL', '')
    _admin_id: ClassVar[str] = os.getenv('TELEGRAM_ADMIN_ID', '')

    @staticmethod
    def _parse_response(response: Union[requests.Response, str]) -> Union[bool, str]:
        if isinstance(response, str):
            return response

        if response.status_code == 200:
            return True
        return (
            'The post to Telegram failed with an error code:'
            f'{response.raise_for_status}'
        )

    @staticmethod
    def _get_exception_message(exc: Exception, *, channel: bool = True) -> str:
        exception_message = (
            'Exception occured during posting to Telegram {receiver}:'
            ' {exc}'
            )
        if channel:
            return exception_message.format(receiver='Channel', exc=exc)

        return exception_message.format(receiver='Admin', exc=exc)

    @staticmethod
    def _send_post(data: Dict[str, str], *, channel: bool = True) -> Union[str, bool]:
        try:
            response: Union[str, requests.Response] = requests.post(
                Telegram._api_url, data=data)
        except Exception as exc:
            response = Telegram._get_exception_message(exc, channel=channel)
        return Telegram._parse_response(response)

    @classmethod
    def _get_data_for_admin(cls, text: str) -> Dict[str, str]:
        return {
            'chat_id': cls._admin_id,
            'text': f'In the channel @{cls._channel}, this message was posted: {text}',
        }

    def _get_data_for_channel(self, text: str) -> Dict[str, str]:
        return {
            'chat_id': f'@{self._channel}',
            'text': text,
        }

    @classmethod
    def post_to_admin(cls, text: str) -> bool:
        data = cls._get_data_for_admin(text)
        response = cls._send_post(data)
        if isinstance(response, str):
            logger.error(response)
        return True

    def send_post(self, *, post_to_channel: bool = True) -> Union[bool, str]:
        # Insert two new lines in-between, make the title bold
        text_to_post = '\n\n'.join(
            [self.post.text, f'*{self.post.title}*', self.post.link])
        data = self._get_data_for_channel(text_to_post)

        if post_to_channel:
            return self._send_post(data, channel=True)

        return self._send_post(data)
