#!/usr/bin/env python3

from .env import CLIENT
from .errors import APIError, BuildError
from .logger import logger


def build_image(
    root: str,
    dockerfile: str,
    tag: str,
):
    try:
        logger.debug(f"building image {tag}")
        img, _ = CLIENT.images.build(
            path=root,
            dockerfile=dockerfile,
            tag=tag,
            rm=True,
        )
    except BuildError as e:
        logger.error(e)
        raise e
    except APIError as e:
        logger.error(e)
        raise e

    return img


class Image(object):
    def __init__(self):
        pass
