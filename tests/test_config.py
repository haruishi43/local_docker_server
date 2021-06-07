#!/usr/bin/env python3

from dhole.config import Config


def test_config():
    config_path = "./tests/configs/test_server.py"

    cfg = Config.fromfile(config_path)

    print(cfg)
