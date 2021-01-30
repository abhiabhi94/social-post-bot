import abc
from typing import Union

from social_post_bot.feeds.processor import Message


class BaseSocialSender(metaclass=abc.ABCMeta):
    def __init__(self, post: Message) -> None:
        self.post = post

    @abc.abstractmethod
    def send_post(self) -> Union[bool, str]:
        raise NotImplementedError
