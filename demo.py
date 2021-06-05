#!/usr/bin/env python3

"""Demo

Testing some functions in this script
TODO move all tests to `tests`!
"""

import docker
from docker.models.containers import Container


def hoge():
    pass


if __name__ == "__main__":
    client = docker.from_env()
    # ret = client.containers.run("alpine", "echo hello world")
    # print(ret)

    containers = client.containers.list()
    print(containers)

    cont = containers[0]
    print(cont.id)

    print(type(cont))
    print(isinstance(cont, Container))

    print(cont.top())
    print(cont.logs())
    print(cont.labels)
