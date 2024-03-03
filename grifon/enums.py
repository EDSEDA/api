import enum
from enum import auto


class AutoName(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self._name_


class ExampleEnum(str, AutoName):
    field1 = auto()
    field2 = auto()
    field3 = auto()
