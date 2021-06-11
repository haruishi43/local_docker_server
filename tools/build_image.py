#!/usr/bin/env python3

import argparse

from dhole.server import ServerV1


config_file = "./configs/demo.py"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help="name of the image to build")
    args = parser.parse_args()
    print(f"building {args.name}")

    server = ServerV1.fromfile(config_file)
    server.build_image(args.name)
