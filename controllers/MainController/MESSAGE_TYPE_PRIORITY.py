"""
File:           MESSAGE_TYPE_PRIORITY.py
Date:           February 2024
Description:    Enumeration of message types associated with their priority levels.
Example of use:
                (msg.message_type = MESSAGE_TYPE_PRIORITY.OK)
                print(msg.message_type)                                   -> MESSAGE_TYPE_PRIORITY.OK -> name of the message
                print(MESSAGE_TYPE_PRIORITY.priority(msg.message_type))   -> 1                        -> priority level of the message

Author:         Nordine HIDA
Modifications:
"""

from enum import Enum, auto


class MESSAGE_TYPE_PRIORITY(Enum):
    """
    Enum class representing message types along with their associated priority levels.
    """
    # Question to ask
    REPORT_STATUS = auto()
    REPORT_POSITION = auto()
    POSITION = auto()

    # Current status asked
    OK = auto()
    STATUS_FREE = auto()
    STATUS_GOTOCOORDINATES = auto()
    PRESENT = auto()
    PRESENT_FREE = auto()

    # Stop everything
    STOP = auto()

    # Tasks
    GO_TO_COORDINATES = auto()
    WHO_IS_PRESENT = auto()
    WHO_IS_PRESENT_AND_FREE = auto()

    @staticmethod
    def priority(msg_type: str) -> int:
        """
        Get the priority associated with a given message type.

        Args:
            msg_type (str): The message type for which to get the priority.

        Returns:
            int: The priority associated with the given message type.

        Raises:
            ValueError: If the message type is not found in the priority mapping.
        """
        priority_mapping = {
            MESSAGE_TYPE_PRIORITY.REPORT_STATUS: 1,
            MESSAGE_TYPE_PRIORITY.REPORT_POSITION: 1,
            MESSAGE_TYPE_PRIORITY.POSITION: 1,
            MESSAGE_TYPE_PRIORITY.OK: 2,
            MESSAGE_TYPE_PRIORITY.STATUS_FREE: 1,
            MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES: 1,
            MESSAGE_TYPE_PRIORITY.PRESENT: 1,
            MESSAGE_TYPE_PRIORITY.PRESENT_FREE: 1,
            MESSAGE_TYPE_PRIORITY.STOP: 1,
            MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES: 1,
            MESSAGE_TYPE_PRIORITY.WHO_IS_PRESENT: 1,
            MESSAGE_TYPE_PRIORITY.WHO_IS_PRESENT_AND_FREE: 1
        }
        try:
            return priority_mapping[MESSAGE_TYPE_PRIORITY.from_string(msg_type)]
        except KeyError:
            raise ValueError("Message type not found in priority mapping")

    @staticmethod
    def from_string(type_string: str):
        """
        Get MESSAGE_TYPE_PRIORITY enum object from string representation.

        Args:
            type_string (str): The string representation of the message type.

        Returns:
            MESSAGE_TYPE_PRIORITY: The corresponding enum object.

        Raises:
            ValueError: If the string representation does not match any enum member.
        """
        enum_name = type_string.split('.')[-1]  # Split by '.', take the last part
        try:
            return MESSAGE_TYPE_PRIORITY[enum_name]
        except KeyError:
            raise ValueError("Invalid message type string")