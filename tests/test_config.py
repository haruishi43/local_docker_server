#!/usr/bin/env python3

from dhole.config import Config


def test_config():
    config_path = "./tests/configs/test_server.py"

    cfg = Config.fromfile(config_path)

    print(cfg)

    # TODO: some other tests
    print(type(cfg))  # Config
    print(type(cfg['server']))  # ConfigDict

    users = cfg.server.users
    user = users[0]

    user_cfg = cfg.get(user)
    print(user_cfg)
    print(type(user_cfg.user1_container1))
    print(user_cfg.keys())
