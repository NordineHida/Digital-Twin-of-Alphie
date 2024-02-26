"""
File:           CommunicationManager.py
Date:           February 2024
Description:    Manage communication between entities (robot, remote, ...)
                Send, receive, order messages.
Author:         Nordine HIDA
Modifications:
"""

from RobotUp import *


class CommunicationManager:
    """
    Manage communication between entities (robot, remote, ...)
    Send, receive, order messages by priority.
    """

    def __init__(self, robot: RobotUp):
        """
        Initialize the CommunicationManager object with the specified robot. \n
        |!| the emitter of the robot should be called "emitter" (default name in webots) \n
        |!| the receiver of the robot should be called "receiver" (default name in webots)

        Args:
            robot (RobotUp): The robot object (a remote can be considered as a robot)
        """
        self.robot = robot
        self.emitter = robot.getDevice("emitter")
        self.receiver = robot.getDevice("receiver")
        self.time_step = int(self.robot.getBasicTimeStep())

    def send_message(self, msg: Message):
        """
        Send a message to the appropriate recipient. \n
        id_sender;message_type;payload
        Args:
            msg (Message): The message to be sent.
        """
        # Construct the message to be sent
        outgoing_msg = "{};{};{}".format(msg.id_sender, msg.message_type, msg.payload)
        print(self.robot.getName(), " : Send : ", outgoing_msg)
        self.emitter.send(outgoing_msg)
        self.robot.step(self.time_step)

    def receive_message(self):
        """
        Receive a message from the communication channel and add it to the robot list of messages.
        As soon as it has been read the message is deleted
        """
        self.robot.step(self.time_step)
        incoming_msg = ""

        if self.receiver.getQueueLength() > 0:
            incoming_msg = self.receiver.getString()
            self.receiver.nextPacket()
        try:
            if incoming_msg != "":
                # Split the incoming message into its three parts
                id_sender, message_type, payload = incoming_msg.split(";")

                print_message_type = message_type.replace("MESSAGE_TYPE_PRIORITY.", "")
                print(self.robot.getName(), " : Receive : ", id_sender, ";", print_message_type, ";", payload)

                # Create and add the Message to the robots list
                self.robot.list_messages.append(Message(id_sender, message_type, payload))

        except ValueError:
            # If there are not enough parts in the message, or it cannot be split properly
            raise ValueError("Invalid message format: '{}'".format(incoming_msg))

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

        return MESSAGE_TYPE_PRIORITY.priority(str(msg.message_type)) > MESSAGE_TYPE_PRIORITY.priority(str(current_task))

    def clear_messages(self):
        """
        Clear all messages in the message's queue and robot's list
        """
        while self.receiver.getQueueLength() > 0:
            self.receiver.nextPacket()
        self.robot.list_messages.clear()
        print(self.robot.getName(), " : All messages cleared")
