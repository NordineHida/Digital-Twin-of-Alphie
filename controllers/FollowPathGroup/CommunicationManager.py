"""
File:          CommunicationManager.py
Date:          February 2024
Description:   Manage all communications between robots to organize them in a network
               (Get all robots, get the next robot to move ...)
Author:        Nordine HIDA
Modifications:
"""


class CommunicationManager:
    """
    A class to manage communication between robots.

    Attributes:
        robot (Robot): The robot instance.
        ordered_list_all_robots (list): A sorted list of robot IDs.
        emitter (Device): Emitter of the robot
        receiver (Device): Receiver of the robot
    """

    def __init__(self, robot):
        """
        Constructs a CommunicationManager object.
        Initialise all devices (emitter,receiver)

        Args:
            robot (Robot): The robot instance.
        """
        self.robot = robot
        self.ordered_list_all_robots = []
        self.emitter = self.robot.getDevice("emitter")
        self.receiver = robot.getDevice("receiver")
        self.receiver.enable(10)

    def send_my_id(self):
        """
        Sends the ID of the current robot all around.
        """
        # TO DO: Implement method
        self.emitter.send("METTRE ICI MISE EN FORME ARNAUD POUR MESSAGE AVEC LE NOM DU ROBOT")


    def send(self,message):
        """
        Sends the message all around.
        """
        # TO DO: Implement method
        self.emitter.send("METTRE ICI MISE EN FORME ARNAUD POUR MESSAGE AVEC LE NOM DU ROBOT")


    def listen_other_id(self):
        """
        Listens for IDs of other robots and updates the ordered list accordingly.
        """
        # TO DO: Implement method
        pass

    def listen(self):
        """
        Listens messages and redirects to the associate methode
        """
        # TO DO: Implement method
        pass

