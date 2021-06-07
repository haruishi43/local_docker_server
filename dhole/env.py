#!/usr/bin/env python3

import docker

from .logger import logger


def init_client():
    logger.debug("initializing client")
    client = docker.from_env()
    return client


CLIENT = init_client()
