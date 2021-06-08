#!/usr/bin/env python3

from .config import Config, ConfigDict


class User:
    def __init__(
        self,
        user_cfg: ConfigDict,
    ) -> None:
        assert isinstance(user_cfg, ConfigDict)
        container_names = list(user_cfg.keys())
