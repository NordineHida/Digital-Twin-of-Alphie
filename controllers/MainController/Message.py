"""
File:           Message.py
Date:           February 2024
Description:    Structure of a message used by robot and remote to communicate.
                A message is composed of 3 parts :
                id_sender;Message_Type;payload

                id_sender = ID (webots's name) of the sender (string)
                MESSAGE_TYPE_PRIORITY = Enumeration of message types associated with their priority levels.
                                        (for more information look MESSAGE_TYPE_PRIORITY.py)
                payload = content of the message (string)

Author:         Nordine HIDA
Modifications:
"""

from MESSAGE_TYPE_PRIORITY import *


class Message:
    """
    Structure of a message used by robot and remote to communicate.
    A message is composed of 3 parts :
    id_sender;MESSAGE_TYPE_PRIORITY;payload

    id_sender = ID (webots's name) of the sender (string)
    MESSAGE_TYPE_PRIORITY = Enumeration of message types associated with their priority levels.
                            (for more information look MESSAGE_TYPE_PRIORITY.py)
    payload = content of the message (string)
    """

    def __init__(self, id_sender: str, message_type: MESSAGE_TYPE_PRIORITY, payload: str):
        """
        Initialize the Message object with provided sender ID, message type, and payload.

        Args:
            id_sender (str): ID of the sender (webots's name).
            message_type (MESSAGE_TYPE_PRIORITY): Message type from the enumeration MESSAGE_TYPE_PRIORITY
            payload (str): Content of the message.
        """
        self.id_sender = id_sender
        self.message_type = message_type
        self.payload = payload


