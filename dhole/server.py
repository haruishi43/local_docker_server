#!/usr/bin/env python3

"""
Server Module
"""

from .config import Config, load_cfg
from .images import ImageCollection
from .users import UserCollection
from .sshconfig import create_sshconfig, dump_sshconfig


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

        # server info
        self.name = cfg.server.name
        self.ip = cfg.server.ip

    @staticmethod
    def fromfile(filename: str):
        cfg = load_cfg(filename)
        return ServerV1(cfg=cfg)

    def output_user_sshconfig(
        self,
        user: str,
    ):
        user = self.users[user]
        s = create_sshconfig(
            name=self.name,
            ip=self.ip,
            containers=user.containers,
        )
        print(s)
        dump_sshconfig(s, self.name)

    def build_images(self):
        # TODO: Parallel
        for image in self.images:
            print(image)
            image.build()

    def run_containers(self):
        containers = self.users.containers
        # TODO: Parallel
        for container in containers:
            print(container)
            container.run()

    def stop_containers(self):
        containers = self.users.containers
        for container in containers:
            container.stop()

    def remove_containers(self, force: bool = False):
        # NOTE: this is very scary
        containers = self.users.containers
        for container in containers:
            container.remove(force=force)

    def remove_unused_images(self):
        for image in self.images:
            image.remove()
