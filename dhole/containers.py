#!/usr/bin/env python3

"""Container Module

Facilitates building contianers as well as managing the users'
containers.
"""

from docker.models.containers import Container as DockerContainer

from .env import CLIENT


class Contianer:
    def __init__(
        self,
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


def create_container():
    pass


def start_container():
    pass


def stop_container():
    pass


def run_container():
    pass


def restart_container():
    pass
