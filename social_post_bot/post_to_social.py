import concurrent.futures
import sys
from typing import List, Optional, Union

from social_post_bot.feeds.processor import Message, process_feed
from social_post_bot.logging_handler import logger
from social_post_bot.socials.fb import Facebook
from social_post_bot.socials.medium import Medium
from social_post_bot.socials.telegram import Telegram
from social_post_bot.socials.tweet import Twitter
from social_post_bot.socials.utils import Socials


class PostSocial(Socials):

    def _get_twitter_post(self, post: Message) -> Optional[Twitter]:
        if self._twitter.do_send:
            return Twitter(post)

        return None

    def _get_medium_post(self, post: Message) -> Optional[Medium]:
        if self._medium.do_send:
            return Medium(post)

        return None

    def _get_telegram_post(self, post: Message) -> Optional[Telegram]:
        if self._telegram.do_send:
            return Telegram(post)

        return None

    def _get_fb_post(self, post: Message) -> Optional[Facebook]:
        if self._facebook.do_send:
            return Facebook(post)

        return None

    def __init__(self, post: Message) -> None:
        self.twitter_post = self._get_twitter_post(post)
        self.medium_post = self._get_medium_post(post)
        self.telegram_post = self._get_telegram_post(post)
        self.fb_post = self._get_fb_post(post)
        self.post = post
        self.response = None

    @staticmethod
    def process_response(*, response: Union[bool, str]) -> str:
        if isinstance(response, bool):
            return 'success'

        return response

    def send_post(self) -> str:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_responses = {
                executor.submit(getattr(self, site.obj).send_post): site
                for site in self._all_socials
                if site.do_send
            }

            responses = {}
            for future_response in concurrent.futures.as_completed(future_responses):
                site = future_responses[future_response]
                responses[site.name] = self.process_response(
                    response=future_response.result())

        response = '\n'.join(
            [f'*{site.title()}*: {response}'for site, response in responses.items()]
        )

        return (
            f'The response of posting the post: {self.post.title} on the'
            f' social sites was:\n{response}'
        )


def _get_posts() -> List[Message]:
    posts = process_feed()
    if not posts:
        msg = 'No new links found. Exiting'
        logger.info(msg)
        sys.exit(msg)
    return posts


def _get_responses() -> List[str]:
    posts = _get_posts()

    responses = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_responses = {
            executor.submit(PostSocial(post).send_post): post
            for post in posts
            }

        for future_response in concurrent.futures.as_completed(future_responses):
            post = future_responses[future_response]
            try:
                responses.append(future_response.result())
            except Exception as exc:
                logger.error(f'{post.title} generated an exception: {exc}')
        return responses


def main() -> None:
    responses = _get_responses()

    complete_response = '\n'.join(responses)

    if Socials._telegram.do_send:
        Telegram.post_to_admin(complete_response)


if __name__ == '__main__':
    main()
