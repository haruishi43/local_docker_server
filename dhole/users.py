#!/usr/bin/env python3

"""
User Module
"""

import os
from typing import Dict, List, Union

from .config import Config, ConfigDict
from .containers import Container, ContainerCollection

__all__ = [
    "UserCollection",
]


class User:
    def __init__(
        self,
        user_name: str,
        user_cfg: ConfigDict,
    ) -> None:
        self.name = user_name
        self.user_cfg = user_cfg

        self.container_collection = ContainerCollection(
            user_cfg=self.user_cfg,
        )

    def __repr__(self) -> str:
        containers = list(self.container_collection.containers.keys())
        return (
            f"User: {self.name}\n"
            f"\t Containers: {containers}\n"
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
            if "container_id" in v.keys():
                containers.append(k)
        assert len(containers) > 0, f"ERR: {self.name} doesn't have any containers"
        return containers

    @property
    def list_images(self) -> List[str]:
        images = []
        for k, v in self.user_cfg.items():
            image_name = v.get("image_name", None)
            if image_name is not None:
                images.append(image_name)
        images = list(set(images))
        assert len(images) > 0, f"ERR: {self.name} doesn't have any images"
        return images


class UserCollection:
    def __init__(
        self,
        cfg: Config,
    ) -> None:
        # initialize users
        users = cfg.server.users
        user_dict = {}
        for user in users:
            assert user not in user_dict.keys(), \
                f"ERR: {user} name is already used, check config"
            user_dict[user] = User(
                user_name=user,
                user_cfg=cfg.get(user),
            )
        self.user_names = users
        self.users = user_dict
        self.user_checks(self.users)

    def __len__(self):
        return len(self.user_names)

    def __getitem__(self, i: Union[str, int]) -> User:
        if isinstance(i, int):
            name = self.user_names[i]
        elif isinstance(i, str):
            name = i
        assert name in self.user_names, f"ERR: {name} is not a valid key"
        return self.users[name]

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
                host_volumes += [v[0] for v in container_values.volumes]
                ports += [p[0] for p in container_values.ports]

        assert len(container_ids) == len(set(container_ids)), \
            f"ERR: has duplicate ids, {container_ids}"
        assert len(ports) == len(set(ports)), \
            f"ERR: has duplicate ports, {ports}"

        # mkdir for host_volumes if it doesn't exist
        for volume in host_volumes:
            if not os.path.exists(volume):
                print(f"WARN: making {volume} because it didn't exist!")
                os.makedirs(volume)

    @property
    def images(self) -> List[str]:
        images = []
        for _, user in self.users.items():
            images += user.list_images
        images = list(set(images))
        return images

    @property
    def containers(self) -> List[Container]:
        containers = []
        for _, user in self.users.items():
            containers += user.containers
        return containers
