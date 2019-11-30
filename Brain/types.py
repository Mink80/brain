from enum import Enum

# Enums
class Type(Enum):
    Info = 0
    Task = 1
    Request = 2

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

# What has been changed during task edit
class TaskChange(Enum):
    Text = 0
    Project = 1
    Type = 2
    DueDate = 3
    Weekly = 4
