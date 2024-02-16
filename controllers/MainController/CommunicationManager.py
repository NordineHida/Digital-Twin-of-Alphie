"""
File:           CommunicationManager.py
Date:           February 2024
Description:    Manage communication between entities (robot, remote, ...)
                Send, receive, order messages.
Author:         Nordine HIDA
Modifications:
"""

from Message import *
from controller.robot import Robot


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
        id_sender;message_type;payload
        Args:
            msg (Message): The message to be sent.
        """
        # Construct the message to be sent
        outgoing_msg = "{};{};{}".format(msg.id_sender, msg.message_type, msg.payload)

        self.emitter.send(outgoing_msg)

    def receive_message(self) -> Message:
        """
        Receive a message from the communication channel.\n
        |!| The format should be : id_sender;MESSAGE_TYPE_PRIORITY;payload

        Returns:
            Message: The received message.
        """
        incoming_msg = self.receiver.getString()

        try:
            # Split the incoming message into its three parts
            id_sender, message_type, payload = incoming_msg.split(";")

            # Create and return a Message object with the extracted parts
            return Message(id_sender, str_to_message_type(message_type), payload)

        except ValueError:
            # If there are not enough parts in the message, or it cannot be split properly
            raise ValueError("Invalid message format: '{}'".format(incoming_msg))

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
        return sorted(list_msg, key=lambda msg: msg.message_type.value, reverse=True)

    @staticmethod
    def is_the_message_prioritary(msg: Message, current_task: MESSAGE_TYPE_PRIORITY) -> bool:
        """
        Process a message to determine if its priority is higher than a current tasks.

        Args:
            msg (Message): The message to be processed.
            current_task (MESSAGE_TYPE_PRIORITY): The current task to compare against.

        Returns:
            bool: True if the message priority is higher than the current task, False otherwise.
        """

        # Compare the priority of the message with the priority threshold
        return msg.message_type.value < current_task.value

    def execute_message(self, msg: Message):
        """
        Execute the message's request

        Args:
            msg (Message): The message to be executed.

        Returns:
            bool: True if the message priority is higher than the current task, False otherwise.
        """

        # Compare the priority of the message with the priority threshold
        pass

    def check_messages(self, current_task: MESSAGE_TYPE_PRIORITY):
        message = self.receive_message()
        # If the robot receives a message that is more prioritized than its current task, it executes the message's task
        if self.is_the_message_prioritary(message,current_task):
            self.execute_message(message)
            print (message, " is prioritized over ", current_task," execution of",current_task , ".")
        # else
            # I should add to a list of order that is stock

