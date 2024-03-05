"""
File:           CommunicationManager.py
Date:           February 2024
Description:    Manage communication between entities (remote, remote, ...)
                Send, receive, order messages.
Author:         Nordine HIDA
Modifications:
"""

from RobotUpRemote import *


class CommunicationManager:
    """
    Manage communication between entities (remote, remote, ...)
    Send, receive, order messages by priority.
    """

    def __init__(self, remote: RobotUpRemote):
        """
        Initialize the CommunicationManager object with the specified remote. \n
        |!| the emitter of the remote should be called "emitter" (default name in webots) \n
        |!| the receiver of the remote should be called "receiver" (default name in webots)

        Args:
            remote (RobotUpRemote): The remote object (a remote can be considered as a remote)
        """
        self.remote = remote
        self.emitter = remote.getDevice("emitter")
        self.receiver = remote.getDevice("receiver")
        self.time_step = int(self.remote.getBasicTimeStep())
        self.max_send_counter = 5

    def send_message(self, msg: Message):
        """
        Send a message to the appropriate recipient. \n
        id_sender;message_type;payload;recipient
        Args:
            msg (Message): The message to be sent.
        """
        # Construct the message to be sent
        outgoing_msg = "{};{};{};{};{}".format(msg.id_sender, msg.message_type, msg.send_counter+1, msg.payload, msg.recipient)
        print(self.remote.getName(), " : Send : ", outgoing_msg)
        self.emitter.send(outgoing_msg)
        self.remote.step(self.time_step)

    def send_message_all(self, id_sender: str, message_type: MESSAGE_TYPE_PRIORITY, send_counter: int, payload: str = ""):
        """
        Send the message to all known robots.
        |!| It didn't mean that they will receive it (they should be in range to receive it)

        Args:
            id_sender (str): ID of the sender (webots's name).
            message_type (MESSAGE_TYPE_PRIORITY): Message type from the enumeration MESSAGE_TYPE_PRIORITY.
            send_counter (int): Number of times the message has been transmitted.
            payload (str): content of the message ("" by default).
        """
        for robot_name in self.remote.known_robots:
            self.send_message(Message(id_sender, message_type, send_counter, payload, robot_name))

    def receive_message(self):
        """
        Receive a message from the communication channel.
        If there is no recipient, or the robot is the recipient, It adds it in its list of messages.
        As soon as it has been read the message is deleted from the receiver's buffer.
        """
        self.remote.step(self.time_step)
        incoming_msg = ""

        if self.receiver.getQueueLength() > 0:
            incoming_msg = self.receiver.getString()
            self.receiver.nextPacket()
        try:
            if incoming_msg != "":
                # Split the incoming message into its three parts
                id_sender, message_type, send_counter, payload, recipient = incoming_msg.split(";")

                # Print of the message (just to check if everything is fine)
                print_message_type = message_type.replace("MESSAGE_TYPE_PRIORITY.", "")
                print(self.remote.getName(), " : Receive : ", id_sender, ";", print_message_type, ";", send_counter, ";", payload, ";", recipient)

                # Create and add the Message to the robots list
                self.remote.append(Message(id_sender, message_type, send_counter, payload, recipient))

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
        self.remote.list_messages.clear()
        print(self.remote.getName(), " : All messages cleared")
