#    Brain!
#    A lightweight web-application for managing tasks in projects
#
#    Copyright 2019, Kai Sassmannshausen
#    Source code repository: https://github.com/Mink80/brain
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
