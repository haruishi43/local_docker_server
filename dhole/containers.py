#!/usr/bin/env python3

"""Container Module

Facilitates building contianers as well as managing the users'
containers.
"""

from typing import Dict, List, Optional, Union

from docker.types import Ulimit

from .config import ConfigDict
from .env import CLIENT
from .logger import logger


# `memlock` and `stack`
DEFAULT_ULIMIT = [
    dict(
        name="memlock",
        soft=-1,  # unlimited
        hard=-1,
    ),
]


class Container:

    def __init__(
        self,
        container_name: str,
        container_id: int,
        image_name: str,
        volumes: Dict[str, Dict[str, str]],
        ports: Dict[str, str],
        labels: Dict[str, str],
        shm_size: Union[str, int] = "32G",
        ulimit: List[Dict[str, Union[str, int]]] = DEFAULT_ULIMIT,
        gpus: Optional[str] = None,  # `runtime` is deprecated (nvidia-docker2)
        **kwargs,
    ) -> None:
        self.name = container_name
        self.id = container_id  # not really used
        self.image = image_name
        self.volumes = volumes
        self.ports = ports
        self.labels = labels
        self.shm_size = shm_size  # usually half of max RAM
        self.ulimit = [Ulimit(**args) for args in ulimit]
        self.gpus = gpus
        self.extra_args = kwargs
        # for extra_args: Dict, see
        # https://docker-py.readthedocs.io/en/stable/containers.html

    def __repr__(self) -> str:
        return (
            f"Container: {self.name} / ID: {self.id}\n"
            f"\tImage: {self.image}\n"
            f"\tVolumes: {self.volumes}\n"
            f"\tPorts: {self.ports}\n"
            f"\tLabels: {self.labels}\n"
        )

    def run(self):
        logger.info(f"Running container {self.name}...")
        container = CLIENT.containers.run(
            image=self.image,
            name=self.name,
            labels=self.labels,
            ports=self.ports,
            volumes=self.volumes,
            detach=True,  # `-d`
            publish_all_ports=True,  # `-P`
            privileged=True,  # `--privileged`
            remove=False,
            shm_size=self.shm_size,
            # stdin_open=True,  # `-t`
            # tty=True,  # `-i`
            **self.extra_args,
        )
        return container

    def create(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def status(self):
        pass

    def delete(self):
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

    def __len__(self) -> int:
        return len(self.containers)

    def __getitem__(self, i: Union[str, int]) -> Container:
        if isinstance(i, int):
            name = list(self.containers.keys())[i]
        elif isinstance(i, str):
            name = i
        assert name in self.containers.keys(), \
            f"ERR: {name} is not in `containers`"
        return self.containers[name]
