#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig as _dictConfig
from os import path

import yaml

__author__ = "Vladimir Keleshev"
__version__ = "2.0rc3"
__description__ = "C generator for language for description of command-line interfaces"


def get_logger(name=None):
    """
    Create logger—with optional name—with the logging.yml config

    :param name: Optional name of logger
    :type name: ```Optional[str]```

    :return: instanceof Logger
    :rtype: ```Logger```
    """
    with open(path.join(path.dirname(__file__), "_data", "logging.yml"), "rt") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    _dictConfig(data)
    return logging.getLogger(name=name)


root_logger = get_logger()

__all__ = ["get_logger", "root_logger"]