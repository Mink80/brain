from enum import Enum

# Enums
class Type(Enum):
    Task = 0
    Request = 1
    Info = 2

class Weekly(Enum):
    No = 0
    Highlight = 1
    Lowlight = 2
    General = 3
    Upcoming = 4

class Model(Enum):
    Task = 0
    Customer = 1
    Partner = 2
    Project = 3

# used for history
class Operation(Enum):
    Added = 0
    Changed = 1
    Deleted = 2
    Undeleted = 3
    Shredded = 4
