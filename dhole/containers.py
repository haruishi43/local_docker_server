#!/usr/bin/env python3

"""Container Module

Facilitates building contianers as well as managing the users'
containers.
"""

from typing import Dict, List, Optional, Tuple, Union

from python_on_whales.utils import DockerException

from .config import ConfigDict
from .env import docker

# `memlock` and `stack`
DEFAULT_ULIMIT = ["memlock=-1:-1"]
STATES = ["created", "restarting", "running", "removing", "paused", "exited", "dead"]


class Container:

    def __init__(
        self,
        container_name: str,
        container_id: int,
        target_user_name: str,
        image_name: str,
        volumes: List[Union[Tuple[str, str, str], Tuple[str, str]]],
        ports: List[Union[Tuple[str, int], Tuple[str, int, str]]],
        labels: Dict[str, str],
        shm_size: Union[str, int] = "32G",
        ulimit: List[str] = DEFAULT_ULIMIT,
        gpus: Optional[Union[str, int]] = None,  # `runtime` is deprecated (nvidia-docker2)
        **kwargs,
    ) -> None:
        """Container class
        """

        # Not really used
        self.id = container_id
        self.target_user_name = target_user_name

        self.name = container_name
        self.image = image_name
        self.volumes = volumes
        self.ports = ports
        self.labels = labels
        self.shm_size = shm_size  # usually half of max RAM
        self.ulimit = ulimit
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
        status = self.check_status()
        if status in STATES:
            print(f"{self.name} is already in state: {status}")
            return docker.container.inspect(self.name)

        print(f"Running container {self.name}...")
        container = docker.run(
            image=self.image,
            name=self.name,
            labels=self.labels,
            publish=self.ports,
            volumes=self.volumes,
            detach=True,  # `-d`
            publish_all=True,  # `-P`
            privileged=True,  # `--privileged`
            remove=False,
            shm_size=self.shm_size,
            ulimit=self.ulimit,
            gpus=self.gpus,
            # stdin_open=True,  # `-t`
            # tty=True,  # `-i`
            **self.extra_args,
        )
        return container

    def check_status(self):
        try:
            container = docker.container.inspect(self.name)
            status = container.state.status
            return status
        except DockerException as e:
            # FIXME: very hacky way to guess if the container has not been created
            if "No such container" in str(e):
                return "not ran"
            else:
                raise e

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
