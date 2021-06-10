#!/usr/bin/env python3

from dhole.server import ServerV1


config_path = "./configs/demo.py"


if __name__ == "__main__":
    user = "user1"
    server = ServerV1.fromfile(config_path)
    server.output_user_sshconfig(user)
