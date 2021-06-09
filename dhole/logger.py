#!/usr/bin/env python3

import logging

__all__ = ["logger"]

_level = logging.DEBUG  # FIXME: change this when it's release
logger = logging.Logger("dhole", encoding="utf-8", level=_level,)
