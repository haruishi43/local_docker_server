#!/usr/bin/env python3

"""
User Module
"""

from copy import deepcopy
import os
from typing import Dict, List

from .config import Config, ConfigDict
from .containers import Container, ContainerCollection
from .logger import logger

__all__ = [
    "UserCollection",
]


def refine_volumes(
    unrefined_volumes: Dict[str, Dict[str, str]],
    user: str,
    target_user_name: str,
) -> Dict[str, Dict[str, str]]:
    """Refine Volumes

    unrefined volumes have string formatting to be done,
    this function formats the strings accordingly
    """
    args = {
        "host_home": os.getenv("HOME"),
        "host_curdir": os.getcwd(),
        "user": user,
        "home": f"/home/{target_user_name}",
    }
    volumes = {}
    for k, v in unrefined_volumes.items():
        key = k.format(**args)
        v["bind"] = v["bind"].format(**args)
        volumes[key] = v
    return volumes


def refine_ports(
    unrefined_ports: Dict[str, int],
    port_id: int,
    container_id: int,
) -> Dict[str, int]:
    """Refine Ports

    unrefined ports have string formatting to be done,
    this function formats the strings accordingly

    NOTE: ports are 5 "digits" long (`{port_id}{access_port}{container_id}`)
    `access_port` is customizable inside the config.
    """
    args = {
        "port_id": str(port_id).zfill(2),
        "container_id": str(container_id).zfill(2),
    }
    ports = {}
    for k, v in unrefined_ports.items():
        key = k.format(**args)
        ports[key] = v
    return ports


def refine_user_cfg(
    user: str,
    cfg: Config,
) -> ConfigDict:
    user_cfg = cfg.get(user)

    containers = list(user_cfg.keys())
    assert len(containers) > 0, \
        f"ERR: {user} must have more than 1 container"

    for container in containers:
        container_cfg = user_cfg.get(container)

        # overwrite the defaults
        container_cfg.volumes.update(cfg.server.volumes)
        container_cfg.ports.update(cfg.server.ports)

        # refine and update dict
        # volumes
        container_cfg.volumes = refine_volumes(
            container_cfg.volumes,
            user=user,
            target_user_name=container_cfg.target_user_name,
        )
        # ports
        container_cfg.ports = refine_ports(
            container_cfg.ports,
            port_id=cfg.server.port_id,
            container_id=container_cfg.container_id,
        )
        # labels
        labels = {}
        labels.update(deepcopy(cfg.labels))
        if "labels" in list(container_cfg.keys()):
            labels.update(deepcopy(container_cfg.labels))
        container_cfg.labels = labels

        user_cfg[container] = container_cfg

    assert isinstance(user_cfg, ConfigDict)

    return user_cfg


def refine_user_cfgs(
    cfg: Config,
) -> Config:
    assert isinstance(cfg, Config), \
        f"ERR: given config is type {type(cfg)} instead of Config"

    users = cfg.server.users
    assert isinstance(users, list), \
        f"ERR: The given variable for `users` is not a list: {users}"
    assert len(users) > 0, "ERR: The given list `users` is empty"

    for user in users:
        cfg[user] = refine_user_cfg(user, cfg)

    assert isinstance(cfg, Config)

    return cfg


class User:
    def __init__(
        self,
        user_name: str,
        user_cfg: ConfigDict,
    ) -> None:
        self.user_name = user_name
        self.user_cfg = user_cfg

        self.container_collection = ContainerCollection(
            user_cfg=self.user_cfg,
        )

    def __len__(self):
        return len(self.containers)

    @property
    def containers(self) -> List[Container]:
        return list(self.container_collection.containers.values())

    @property
    def list_containers(self) -> List[str]:
        # FIXME: user_cfg might contain other keys than containers
        containers = []
        for k, v in self.user_cfg.items():
            # for now, just check if the container has container_id, which is unique
            if "container_id" in list(v.keys()):
                containers.append(k)
        assert len(containers) > 0, f"ERR: {self.user_name} doesn't have any containers"
        return containers

    @property
    def list_images(self) -> List[str]:
        images = []
        for k, v in self.user_cfg.items():
            image_name = v.get("image_name", None)
            if image_name is not None:
                images.append(image_name)
        images = list(set(images))
        assert len(images) > 0, f"ERR: {self.user_name} doesn't have any images"
        return images


class UserCollection:
    def __init__(
        self,
        cfg: Config,
    ) -> None:
        # refine cfg
        cfg = refine_user_cfgs(cfg)

        # initialize users
        users = cfg.server.users
        user_dict = {}
        for user in users:
            assert user not in list(user_dict.keys()), \
                f"ERR: {user} name is already used, check config"
            user_dict[user] = User(
                user_name=user,
                user_cfg=cfg.get(user),
            )
        self._user_dict = user_dict

        # self.user_checks(self._user_dict)

    def __len__(self):
        return len(self._user_dict)

    def __getitem__(self, i):
        # FIXME: does this work?
        user = self.user_dict.values()[i]
        return user

    @staticmethod
    def user_checks(users: Dict[str, User]) -> None:
        """Do some checks of the User
        """
        container_ids = []
        host_volumes = []
        ports = []
        for _, user in users.items():
            for _, container_values in user.user_cfg.items():
                container_ids.append(container_values.container_id)
                host_volumes += list(container_values.volumes.keys())
                ports += list(container_values.ports.keys())

        assert len(container_ids) == len(set(container_ids)), \
            f"ERR: has duplicate ids, {container_ids}"
        assert len(ports) == len(set(ports)), \
            f"ERR: has duplicate ports, {ports}"

        # mkdir for host_volumes if it doesn't exist
        for volume in host_volumes:
            if not os.path.exists(volume):
                logger.warning(f"WARN: making {volume} because it didn't exist!")
                os.makedirs(volume)

    @property
    def users(self) -> List[str]:
        return list(self._user_dict.keys())

    @property
    def images(self) -> List[str]:
        images = []
        for _, user in self._user_dict.items():
            images += user.images
        images = list(set(images))
        return images

    @property
    def containers(self) -> List[Container]:
        containers = []
        for name, user in self._user_dict.items():
            containers += user.containers
        return containers
