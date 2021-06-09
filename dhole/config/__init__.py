#!/usr/bin/env python3

from .config import Config, ConfigDict
from .loader import load_cfg

__all__ = [
    "Config",
    "ConfigDict",
    "load_cfg",
]
