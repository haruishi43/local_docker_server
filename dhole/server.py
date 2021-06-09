#!/usr/bin/env python3

"""
Server Module
"""

from .config import Config, load_cfg
from .images import ImageCollection
from .logger import logger
from .users import UserCollection


class ServerV1:
    def __init__(
        self,
        cfg: Config,
    ) -> None:
        self.users = UserCollection(cfg=cfg)
        images = self.users.images
        self.images = ImageCollection(
            images=images,
            cfg=cfg,
        )

    @staticmethod
    def fromfile(filename: str):
        cfg = load_cfg(filename)
        return ServerV1(cfg=cfg)

    def build_images(self):
        for image in self.images:
            logger.info(image)
            image.build()

    def run_containers(self):
        containers = self.users.containers
        for container in containers:
            logger.info(container)
            container.run()
