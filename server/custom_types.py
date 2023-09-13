import enum


# values might need to be string and not integers
class Priority(enum.Enum):
    """
    priority custom type.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(enum.Enum):
    """
    status custom type.
    """

    READY = 1
    IN_PROGRESS = 2
    PAUSED = 3
    BLOCKED = 4
    DONE = 5
