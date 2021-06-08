#!/usr/bin/env python3

"""
Server Module
"""

from copy import deepcopy
import os
from typing import Any, Dict

from .config import Config
from .logger import logger


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


class Server:

    @staticmethod
    def fromfile(filename: str):
        cfg = Config.fromfile(filename)
        return Server(cfg=cfg)

    def __init__(
        self,
        cfg: Config,
    ) -> None:
        assert isinstance(cfg, Config)

        server_cfg = cfg.server.deepcopy()
        assert len(server_cfg) > 0

        users = server_cfg.users
        assert isinstance(users, list)
        assert len(users) > 0

        volumes = deepcopy(server_cfg.volumes)
        ports = deepcopy(server_cfg.ports)
        labels = deepcopy(server_cfg.labels)

        _users = {}
        for user in users:
            user_cfg = cfg.get(user)

            containers = list(user_cfg.keys())
            assert len(containers) > 0

            for container in containers:
                container_cfg = user_cfg.get(container)

                # overwrite the defaults
                container_cfg.volumes.update(volumes)
                container_cfg.ports.update(ports)

                # refine and update dict
                container_cfg.volumes = refine_volumes(
                    container_cfg.volumes,
                    user=user,
                    target_user_name=container_cfg.target_user_name,
                )
                container_cfg.ports = refine_ports(
                    container_cfg.ports,
                    port_id=server_cfg.port_id,
                    container_id=container_cfg.container_id,
                )
                container_cfg.labels = labels

            # FIXME: create User instance instead?
            _users[user] = user_cfg.deepcopy()

        self.users = _users
        self.cfg = cfg
        self.server_cfg = server_cfg

    @staticmethod
    def user_checks(users: Dict[str, Dict[str, Any]]) -> None:
        """Do some checks of the user config
        """
        container_ids = []
        host_volumes = []
        ports = []
        for _, containers in users.items():
            for _, container_values in containers.items():
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

    def build_images(self):
        pass

    def run_containers(self):
        pass
