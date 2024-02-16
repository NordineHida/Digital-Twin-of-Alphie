"""
File:           CommunicationManager.py
Date:           February 2024
Description:    Manage communication between entities (robot, remote, ...)
                Send, receive, order messages.
Author:         Nordine HIDA
Modifications:
"""

from Message import *
from controller.robot import *


class CommunicationManager:
    """
    Manage communication between entities (robot, remote, ...)
    Send, receive, order messages.
    """

    def __init__(self, robot: Robot):
        """
        Initialize the CommunicationManager object with the specified robot. \n
        |!| the emitter of the robot should be called "emitter" (default name in webots) \n
        |!| the receiver of the robot should be called "receiver" (default name in webots)

        Args:
            robot (Robot): The robot object (a remote can be considered as a robot)
        """
        self.robot = robot
        self.emitter = robot.getDevice("emitter")
        self.receiver = robot.getDevice("receiver")

    def send_message(self, msg: Message):
        """
        Send a message to the appropriate recipient. \n

        Args:
            msg (Message): The message to be sent.
        """
        # Construct the message to be sent
        outgoing_msg = "{};{};{}".format(msg.id_sender, msg.message_type, msg.payload)

        self.emitter.send(outgoing_msg)

    def receive_message(self) -> Message:
        """
        Receive a message from the communication channel.\n
        |!| The format should be : id_sender;Message_Type;payload

        Returns:
            Message: The received message.
        """
        incoming_msg = self.receiver.getString()

        try:
            # Split the incoming message into its three parts
            id_sender, message_type, payload = incoming_msg.split(";")

            # Create and return a Message object with the extracted parts
            return Message(id_sender, Memessage_type, payload)

        except ValueError:
            # If there are not enough parts in the message, or it cannot be split properly
            raise ValueError("Invalid message format: '{}'".format(incoming_msg))

        except Exception as e:
            # Handle any other unexpected errors
            raise Exception("An error occurred while processing the message: {}".format(str(e)))

    @staticmethod
    def ordered_messages_by_priority(list_msg: list[Message]) -> list[Message]:
        """
        Order a list of messages by priority (in descending order).

        Args:
            list_msg (list[Message]): List of messages to be ordered.

        Returns:
            list[Message]: List of messages ordered by priority.
        """
        # Sort the list of messages by priority in descending order
        return sorted(list_msg, key=lambda msg: msg.message_type.get_message_priority(), reverse=True)

