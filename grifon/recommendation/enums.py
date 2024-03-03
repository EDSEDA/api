from enum import auto

from grifon.enums import AutoName


class ExampleEnum(str, AutoName):
    field1 = auto()
    field2 = auto()
    field3 = auto()
