#!/usr/bin/env python3

"""Container Module

Facilitates building contianers as well as managing the users'
containers.
"""

from typing import Dict
from docker.models.containers import Container as DockerContainer

from .config import ConfigDict
from .env import CLIENT


class Container:
    def __init__(
        self,
        container_name: str,
        container_id: int,
        image_name: str,
        volumes: Dict[str, Dict[str, str]],
        ports: Dict[str, str],
        labels: Dict[str, str],
    ) -> None:
        # pass server config and user config
        # append `ip`, `port_id`, `volumes` to config
        pass

    def create(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def run(self):
        pass

    def status(self):
        pass


class ContainerCollection:
    def __init__(
        self,
        user_cfg: ConfigDict,
    ) -> None:
        containers = {}
        for name, cfg in user_cfg.items():
            containers[name] = Container(
                container_name=name,
                **cfg,
            )
        self.containers = containers
