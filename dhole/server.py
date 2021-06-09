#!/usr/bin/env python3

"""
Server Module
"""

from .config import Config
from .images import ImageCollection
from .users import UserCollection


class Server:

    @staticmethod
    def fromfile(filename: str):
        cfg = Config.fromfile(filename)
        return Server(cfg=cfg)

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

    def build_images(self):
        pass

    def run_containers(self):
        pass
