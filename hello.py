#!/usr/bin/env python3

import numpy as np

some_global_variable = 1


def hello():
    some_local_variable = 0
    print(locals())


if __name__ == "__main__":
    print(globals())
    hello()
