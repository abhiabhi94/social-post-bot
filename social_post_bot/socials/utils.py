from typing import NamedTuple, List, ClassVar
import os


class Social(NamedTuple):
    do_send: bool
    obj: str
    name: str


class Socials:
    _medium = Social(
        do_send=bool(os.getenv('USE_MEDIUM', True)),
        obj='medium_post',
        name='Medium'
    )
    _twitter = Social(
        do_send=bool(os.getenv('USE_TWITTER', True)),
        obj='twitter_post',
        name='Twitter'
    )

    _telegram = Social(
        do_send=bool(os.getenv('USE_TELEGRAM', True)),
        obj='telegram_post',
        name='Twitter'
    )

    _facebook = Social(
        do_send=bool(os.getenv('USE_FACEBOOK', True)),
        obj='fb_post',
        name='Facebook'
    )

    _all_socials: ClassVar[List[Social]] = [_medium, _twitter, _telegram, _facebook]
