#!/usr/bin/env python3

from dhole.config import Config
from dhole.server import Server


def test_server():
    cfg_file = "./tests/configs/test_server.py"
    cfg = Config.fromfile(cfg_file)
    server = Server(cfg=cfg)

    server.user_checks(server.users)
