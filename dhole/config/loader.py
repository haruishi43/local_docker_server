#!/usr/bin/env python3

"""Loader Module

loading the config and changing some variables inside the config
so that it can be used without anymore refinements.
"""

from copy import deepcopy
import os
from typing import Dict, Union

from .config import Config, ConfigDict

__all__ = ["load_cfg"]


def _check_key(key: str, cfg: Union[Config, ConfigDict, dict]) -> None:
    """Check for key in dict-like objects
    """
    assert key in cfg.keys(), \
        f"ERR: {key} is not in {list(cfg.keys())}"


def _fill_volumes_with_string(
    unrefined_volumes: Dict[str, Dict[str, str]],
    user: str,
    target_user_name: str,
) -> Dict[str, Dict[str, str]]:
    """Refine Volumes

    unrefined volumes have string formatting to be done,
    this function formats the strings accordingly

    For now you can use:
    - `host_home`: $HOME
    - `host_curdir`: pwd
    - `user`: name of the user
    - `home`: target home; ususally `/home/ubuntu`
    """
    args = {
        "host_home": os.getenv("HOME"),
        "host_curdir": os.getcwd(),
        "user": user,
        "home": f"/home/{target_user_name}",
    }
    volumes = {}
    for k, v in deepcopy(unrefined_volumes).items():
        key = k.format(**args)
        v = v["bind"].format(**args)
        volumes[key] = v
    return volumes


def _fill_ports_with_strings(
    unrefined_ports: Dict[str, int],
    port_id: int,
    container_id: int,
) -> Dict[str, int]:
    """Refine Ports

    unrefined ports have string formatting to be done,
    this function formats the strings accordingly

    For now, you can use:
    - `port_id`
    - `container_id`

    NOTE: ports are 5 "digits" long (`{port_id}{access_port}{container_id}`)
    `access_port` is customizable inside the config.
    """

    # some assertions
    assert port_id > 0 and port_id < 10, \
        f"ERR: check range for `port_id`, {port_id} is invalid"
    assert container_id >= 0 and container_id < 100, \
        f"ERR: check range for `container_id`, {container_id} is invalid"

    args = {
        "port_id": str(port_id),
        "container_id": str(container_id).zfill(2),
    }
    ports = {}
    for k, v in deepcopy(unrefined_ports).items():
        key = k.format(**args)
        ports[key] = v
    return ports


def _refine_user_cfg(
    user: str,
    cfg: Config,
) -> ConfigDict:
    """Refine 1 user ConfigDict
    """

    user_cfg = cfg.get(user)

    containers = list(user_cfg.keys())
    assert len(containers) > 0, \
        f"ERR: {user} must have more than 1 container"

    for container in containers:
        container_cfg = user_cfg.get(container)

        # Do some basic checks for keys and formatting
        _check_key("container_id", container_cfg)
        _check_key("image_name", container_cfg)
        _check_key("target_user_name", container_cfg)

        # overwrite the defaults
        raw_volumes = {}
        raw_ports = {}
        labels = {}
        if "volumes" in cfg.server.keys():
            raw_volumes.update(cfg.server.volumes)
        if "volumes" in container_cfg.keys():
            raw_volumes.update(container_cfg.volumes)
        if "ports" in cfg.server.keys():
            raw_ports.update(cfg.server.ports)
        if "ports" in container_cfg.keys():
            raw_ports.update(container_cfg.ports)
        assert "labels" in cfg.keys(), \
            "ERR: `labels` should be `cfg`"
        labels.update(deepcopy(cfg.labels))
        if "labels" in container_cfg.keys():
            labels.update(deepcopy(container_cfg.labels))

        # volumes
        container_cfg.volumes = _fill_volumes_with_string(
            raw_volumes,
            user=user,
            target_user_name=container_cfg.target_user_name,
        )
        # ports
        container_cfg.ports = _fill_ports_with_strings(
            raw_ports,
            port_id=cfg.server.port_id,
            container_id=container_cfg.container_id,
        )
        # labels
        container_cfg.labels = labels

        user_cfg[container] = container_cfg

    assert isinstance(user_cfg, ConfigDict)

    return user_cfg


def load_cfg(cfg_file: str):
    """Load config and organize dictionaries
    """
    cfg = Config.fromfile(cfg_file)

    assert isinstance(cfg, Config), \
        f"ERR: given config is type {type(cfg)} instead of Config"

    # Do basic key checks and basic format of the cfg
    # root
    _check_key("image_path", cfg)
    _check_key("labels", cfg)
    _check_key("server", cfg)
    # server
    _check_key("ip", cfg.server)
    _check_key("port_id", cfg.server)
    _check_key("users", cfg.server)
    _check_key("ports", cfg.server)  # TODO: might need a specific check for port 22

    # Do basic checks for server.users
    users = cfg.server.users
    assert isinstance(users, list), \
        f"ERR: The given variable for `users` is not a list: {users}"
    assert len(users) > 0, "ERR: The given list `users` is empty"
    assert (len(set(users)) == len(users)) and \
        (len(set(map(str.lower, users))) == len(users)), \
        f"ERR: The list of users, {users} might have duplicates"

    # Convert user config (substitute strings from `server`)
    for user in users:
        _check_key(user, cfg)
        cfg[user] = _refine_user_cfg(user, cfg)

    assert isinstance(cfg, Config)

    return cfg
