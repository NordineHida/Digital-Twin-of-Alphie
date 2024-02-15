"""
File:           Message_Type.py
Date:           February 2024
Description:    Dictionary of message types. Each message type is represented by an id_message
                serving as the key, and the corresponding string represents the message type.

                Additionally, each message type is associated with a priority represented by an integer value.
                This priority information is stored in a separate dictionary where the name of the message
                is associated with its priority level. This prioritization system enables the execution of
                messages based on their priority levels.

Author:         Nordine HIDA
Modifications:
"""


class Message_Type:
    """
    Class representing a dictionary of message types with associated priorities.
    """

    def __init__(self):
        """
        Initialize the Message_Type object with predefined message types and their respective priorities.
        """
        # Predefined dictionary of message types with their codes
        # int codes come from the arduino program of robots
        self.message_type = {
            # Status
            0000: "OK",
            101: "REPORT_STATUS",
            102: "STATUS",
            103: "REPORT_ERRORS",
            104: "ERROR",
            105: "REPORT_POSITION",
            106: "POSITION",
            107: "ABORT",
            108: "PRESENT",
            109: "PRESENT_FREE",

            # Movement
            10: "FORWARD",
            11: "BACKWARD",
            12: "TURN_LEFT",
            13: "TURN_RIGHT",
            14: "FORWARD_TURN",
            15: "BACKWARD_TURN",
            17: "STOP",

            # Tasks
            110: "TURN_TOWARDS",
            111: "GO_TO_COORDINATES",
            112: "WHO_IS_PRESENT",
            113: "WHO_IS_PRESENT_AND_FREE"
        }

        # Dictionary to store message priorities
        self.message_priority = {
            "OK": 1,
            "REPORT_STATUS": 1,
            "STATUS": 1,
            "REPORT_ERRORS": 1,
            "ERROR": 1,
            "REPORT_POSITION": 1,
            "POSITION": 1,
            "ABORT": 1,
            "FORWARD": 1,
            "BACKWARD": 1,
            "TURN_LEFT": 1,
            "TURN_RIGHT": 1,
            "FORWARD_TURN": 1,
            "BACKWARD_TURN": 1,
            "STOP": 1,
            "TURN_TOWARDS": 1,
            "GO_TO_COORDINATES": 1,
            "RAW": 1,
            "INVALID": 1,
            "WHO_IS_PRESENT": 1,
            "PRESENT": 1,
            "WHO_IS_PRESENT_AND_FREE": 1,
            "PRESENT_FREE": 1
        }

    def get_message(self, id_message: int) -> str:
        """
        Retrieve the message type associated with the given message ID.

        Args:
            id_message (int): The message ID.

        Returns:
            str: The message type associated with the given ID.

        Raises:
            KeyError: If the provided message ID does not exist in the message_type dictionary.
        """
        try:
            return self.message_type[id_message]
        except KeyError:
            raise KeyError("Message ID not found.")

    def get_message(self, message: str) -> int:
        """
        Retrieve the message ID associated with the given message type.

        Args:
            message (str): The message type.

        Returns:
            int: The message ID associated with the given message type.

        Raises:
            ValueError: If the provided message type does not exist in the message_type dictionary.
        """
        try:
            return next(key for key, value in self.message_type.items() if value == message)
        except StopIteration:
            raise ValueError("Message type not found.")

    def get_message_priority(self, message: str) -> int:
        """
        Retrieve the priority level associated with the given message type.

        Args:
            message (str): The message type.

        Returns:
            int: The priority level associated with the given message type.

        Raises:
            KeyError: If the provided message type does not exist in the message_priority dictionary.
        """
        try:
            return self.message_priority[message]
        except KeyError:
            raise KeyError("Message type not found.")

    def get_message_priority(self, id_message: int) -> int:
        """
        Retrieve the priority level associated with the given message code.

        Args:
            id_message (int): The message code.

        Returns:
            int: The priority level associated with the given message code.

        Raises:
            KeyError: If the provided message code does not exist in the message_type dictionary.
        """
        try:
            message_type = self.get_message(id_message)
            return self.message_priority[message_type]
        except KeyError:
            raise KeyError("Message code not found.")
