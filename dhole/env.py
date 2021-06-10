#!/usr/bin/env python3

from python_on_whales import DockerClient


def init_docker():
    print("initializing client")
    docker = DockerClient()
    return docker


docker = init_docker()
