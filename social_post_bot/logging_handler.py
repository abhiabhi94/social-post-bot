import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('social_post_bot')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('social_post_bot.log')
fh.setLevel(logging.DEBUG)

fh.setFormatter(formatter)

logger.addHandler(fh)
