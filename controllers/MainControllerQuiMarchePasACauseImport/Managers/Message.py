"""
File:           Message.py
Date:           February 2024
Description:    Structure of a message used by robot and remote to communicate.
                A message is composed of 3 parts :
                id_sender;Message_Type;payload

                id_sender = ID (webots's name) of the sender (string)
                Message_Type = dictionary which associate an id_message
                with a string representing the message (for more information look MESSAGE_TYPE_PRIORITY.py)
                payload = content of the message (string)

Author:         Nordine HIDA
Modifications:
"""

from Message_Type import Message_Type


class Message:
    """
    Structure of a message used by robot and remote to communicate.
    A message is composed of 3 parts :
    id_sender;Message_Type;payload

    id_sender = ID (webots's name) of the sender (string)
    Message_Type = dictionary which associate a code (composed of 4 digits max)
                    with a string representing the message (for more information look MESSAGE_TYPE_PRIORITY.py)
    payload = content of the message (string)
    """

    def __init__(self, id_sender: str, message_type: Message_Type, payload: str):
        """
        Initialize the Message object with provided sender ID, message type, and payload.

        Args:
            id_sender (str): ID of the sender (webots's name).
            message_type (Message_Type): Instance of Message_Type class representing the message type.
            payload (str): Content of the message.
        """
        self.id_sender = id_sender
        self.message_type = message_type
        self.payload = payload
