#!/usr/bin/env python3

"""Tests for Config (and related modules)

- Edge failure cases for configuration files seem really hard to code (too lazy
  to code every little cases). I hope the assertions inside `loader.py` can catch
  most of the failure cases.
- The tedious cases that needs testing are:
  - subsitutions in strings ("{foo}".format(foo="bar"))
  - cases where there are no `volume` (need to check if the container runs without it)
  - checks for `ports` (there must be a port 22)
- Just check for one default success case and a couple failure cases that I might want to
  catch.
"""

from dhole.config import Config, load_cfg


def test_config():
    config_path = "./tests/configs/test_server.py"

    cfg = load_cfg(config_path)

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
