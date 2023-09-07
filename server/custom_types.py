import enum
from sqlalchemy import Enum

# values might need to be string and not integers
class Priority(enum.Enum):
    low = 1
    medium = 2
    high = 3

class Status(enum.Enum):
    ready = 1
    in_propgres = 2
    paused = 3
    blocked = 4
    done = 5