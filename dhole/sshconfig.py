#!/usr/bin/env python3

import os
from typing import List

from dhole.containers import Container


def create_sshconfig(
    name: str,
    ip: str,
    containers: List[Container],
    connection_port_num: int = 22,  # host connection port
) -> str:
    """Create .ssh/config_{name} for an user

    formating:

    ```
    Host {name}-{container.name stripped of user.name}
        HostName {ip}
        User {container.target_user_name}
        Port {container.port where port==22}
        TCPKeepAlive yes
    ```
    """

    header = f"# SSH Containers for {name}\n"

    base = (
        "\n\n"
        "Host {name}-{container_name}\n"
        "    HostName {ip}\n"
        "    User {target_user_name}\n"
        "    Port {connection_port}\n"
        "    TCPKeepAlive yes"
    )

    sl = header

    for container in containers:
        container_name = container.name.split("_")[-1]  # get the container name
        target_user_name = container.target_user_name
        ports = container.ports
        connection_port = None
        for port in ports:
            if port[1] == connection_port_num:
                connection_port = port[0]
        assert connection_port is not None, \
            [
                f"ERR: port {connection_port_num} is not in ports for {container.name}\n"
                f"\tPorts: {ports}\n"
            ]
        sl += base.format(
            name=name,
            container_name=container_name,
            ip=ip,
            target_user_name=target_user_name,
            connection_port=connection_port,
        )

    return sl


def dump_sshconfig(
    config: str,
    server_name: str,
) -> None:
    """Will be saved as `~/.ssh/config_{server_name}`
    """
    fp = os.path.join(os.getenv("HOME"), ".ssh", f"config_{server_name}")
    with open(fp, "w+") as f:
        f.write(config)
    os.chmod(fp, 0o664)  # change permission!
