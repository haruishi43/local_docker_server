#!/usr/bin/env python3

from dhole.config import load_cfg
from dhole.server import ServerV1

config_path = "./configs/demo.py"


if __name__ == "__main__":
    cfg = load_cfg(config_path)

    server = ServerV1(cfg)
    # server.build_images()

    for user in server.users:
        print(user)
