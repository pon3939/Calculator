# -*- coding: utf8 -*-

from enum import Enum, auto

"""
命令の定数クラス
"""


class Operation(Enum):
    """
    命令の定数クラス
    """

    INITIAL = auto()
    ADDITION = auto()
    SUBTRACT = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    EQUAL = auto()
