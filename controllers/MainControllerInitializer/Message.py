"""
File:           Message.py
Date:           February 2024
Description:    Structure of a message used by robot and remote to communicate.
                A message is composed of 4 parts :
                id_sender;Message_Type;payload

                id_sender = ID (webots's name) of the sender (string)
                MESSAGE_TYPE_PRIORITY = Enumeration of message types associated with their priority levels.
                                        (for more information look MESSAGE_TYPE_PRIORITY.py)
                send_counter (int): Number of times the message has been transmitted.
                payload = content of the message ("" by default) (string)
                recipient = recipient of the message (webots's name). It can be empty ("" by default)(string)
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
    send_counter (int): Number of times the message has been transmitted.
    payload = content of the message ("" by default) (string)
    recipient = recipient of the message (webots's name). It can be empty ("" by default)(string)
    """

    def __init__(self, id_sender: str, message_type: MESSAGE_TYPE_PRIORITY, send_counter: int, payload: str = "", recipient: str = ""):
        """
        Initialize the Message object with provided sender ID, message type, and payload, and maybe a recipient.

        Args:
            id_sender (str): ID of the sender (webots's name).
            message_type (MESSAGE_TYPE_PRIORITY): Message type from the enumeration MESSAGE_TYPE_PRIORITY.
            payload (str): content of the message ("" by default).
            send_counter (int): Number of times the message has been transmitted.
            recipient (str): recipient of the message (webots's name). It can be empty ("" by default).
        """
        self.id_sender = id_sender
        self.message_type = message_type
        self.send_counter = send_counter
        self.payload = payload
        self.recipient = recipient
