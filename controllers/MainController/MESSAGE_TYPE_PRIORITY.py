"""
File:           MESSAGE_TYPE_PRIORITY.py
Date:           February 2024
Description:    Enumeration of message types associated with their priority levels.
Example of use:
                print(MESSAGE_TYPE_PRIORITY.OK)         -> MESSAGE_TYPE_PRIORITY.OK -> name of the message
                print(MESSAGE_TYPE_PRIORITY.OK.value)   -> 1                        -> priority level of the message

Author:         Nordine HIDA
Modifications:
"""

from enum import Enum


class MESSAGE_TYPE_PRIORITY(Enum):
    """
    Enum class representing message types along with their associated priority levels.
    """
    # Status
    OK = 1
    REPORT_STATUS = 1
    STATUS = 1
    REPORT_ERRORS = 1
    ERROR = 1
    REPORT_POSITION = 1
    POSITION = 1
    ABORT = 1

    STATUS_GOTOCOORDINATES = 1
    PRESENT = 1
    PRESENT_FREE = 1

    # Movement
    FORWARD = 1
    BACKWARD = 1
    TURN_LEFT = 1
    TURN_RIGHT = 1
    STOP = 1

    # Tasks
    GO_TO_COORDINATES = 1
    WHO_IS_PRESENT = 1
    WHO_IS_PRESENT_AND_FREE = 1


def str_to_message_type(msg_string: str) -> MESSAGE_TYPE_PRIORITY:
    """
    Convert a string to a member of MESSAGE_TYPE_PRIORITY.

    Args:
        msg_string (str): String representing the message type.

    Returns:
        MESSAGE_TYPE_PRIORITY: Corresponding member of the MESSAGE_TYPE_PRIORITY enumeration.

    Raises:
        ValueError: If the string is not a valid member of MESSAGE_TYPE_PRIORITY.
    """
    try:
        return MESSAGE_TYPE_PRIORITY[msg_string]
    except KeyError:
        raise ValueError(f"{msg_string} is not a member of MESSAGE_TYPE_PRIORITY, please check MESSAGE_TYPE_PRIORITY.py")
