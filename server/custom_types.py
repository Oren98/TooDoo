import enum

# values might need to be string and not integers
class Priority(enum.Enum):
    """
    priority custom type.
    """
    low = 1
    medium = 2
    high = 3

class Status(enum.Enum):
    """
    status custom type.
    """
    ready = 1
    in_propgres = 2
    paused = 3
    blocked = 4
    done = 5