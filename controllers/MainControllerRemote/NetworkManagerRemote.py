"""
File:           NetworkManagerRemote.py
Date:           February 2024
Description:    Manage the network of communication between the remote and robots
Author:         Nordine HIDA
Modifications:
"""

from CommunicationManager import *


class NetworkManagerRemote:
    """
    Manage the network of communication between the remote and robots.
    It sends messages bound to keys and reacts to incoming messages.
    """

    def __init__(self, robot: RobotUp):
        """
        Initialize the NetworkManager.

        Args:
            robot (Robot): The robot (a remote can be considered as a robot)
        """
        self.robot = robot
        self.robot_name = self.robot.getName()

        self.communication = CommunicationManager(self.robot)

        # Initialize the keyboard
        self.keyboard = self.robot.getKeyboard()
        self.keyboard.enable(10)

    def update(self):
        """
        Check if there is message or a pressed key and handle it.
        """

        # Check if a key is pressed
        key = self.keyboard.getKey()
        if key != -1:
            # Home -> REPORT_BEGIN_ROLLCALL
            if key == Keyboard.HOME:
                self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL, ""))
                self.robot.is_callrolling = True
            # END -> STOP
            if key == Keyboard.END:
                self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.STOP, ""))
            # Arrow keys -> GO_TO_COORDINATES with different coordinates
            if key == Keyboard.RIGHT:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, "1:1"))
            if key == Keyboard.UP:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, "1:-1"))
            if key == Keyboard.LEFT:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, "-1:1"))
            if key == Keyboard.DOWN:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, "-1:-1"))

            # Page down -> Path which form a circle around (0;0)
            if key == Keyboard.PAGEDOWN:
                import math

                # Center of the circle
                center_x = 0
                center_y = 0

                # Radius of the circle
                radius = 1.5

                # Number of points to generate
                num_points = 20

                for i in range(num_points):
                    # Calculate angle for each point
                    angle = 2 * math.pi * i / num_points

                    # Calculate coordinates for each point
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)

                    # Sending message to go to coordinates
                    message = Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, f"{x}:{y}")
                    self.communication.send_message(message)

        # try to receive a message and add it to the robot's list
        self.communication.receive_message()

        # Check if the list of messages is not empty
        if self.robot.list_messages:
            # Getting the first message and remove it from the list
            message = self.robot.list_messages[0]
            self.robot.list_messages.pop(0)

            id_sender = message.id_sender
            message_type = MESSAGE_TYPE_PRIORITY.from_string(message.message_type)
            payload = message.payload

            match message_type:
                case MESSAGE_TYPE_PRIORITY.REPORT_STATUS:
                    self.case_REPORT_STATUS(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_POSITION:
                    self.case_REPORT_POSITION(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES:
                    self.case_STATUS_GOTOCOORDINATES(id_sender)

                case MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                    self.case_STATUS_FREE(id_sender)

                case MESSAGE_TYPE_PRIORITY.STOP:
                    self.case_STOP()

                case MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES:
                    self.case_GO_TO_COORDINATES(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL:
                    self.case_REPORT_BEGIN_ROLLCALL(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_END_ROLLCALL:
                    self.case_REPORT_END_ROLLCALL()

                case MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE:
                    pass

                case _:
                    print("Unknown message received")

            self.update_prev_next_robot()

    def update_prev_next_robot(self):
        """
        Update the previous and next robots based on the robot's name and known_robots dictionary.

        This method looks into the known_robots dictionary to find the key (robot name) just before and just after
        the current robot's name (self.robot_name). It then updates the prev_rob and next_rob attributes accordingly.
        """
        sorted_robots = sorted(self.robot.known_robots.keys())
        current_index = sorted_robots.index(self.robot_name)

        if current_index > 0:
            self.robot.prev_rob = sorted_robots[current_index - 1]
        else:
            self.robot.prev_rob = None

        if current_index < len(sorted_robots) - 1:
            self.robot.next_rob = sorted_robots[current_index + 1]
        else:
            self.robot.next_rob = None

    def case_REPORT_STATUS(self, id_sender, payload):
        # TODO: Implement handling of REPORT_STATUS message
        pass

    def case_REPORT_POSITION(self, id_sender, payload):
        # TODO: Implement handling of REPORT_POSITION message
        pass

    def case_STATUS_GOTOCOORDINATES(self, id_sender):
        self.robot.known_robots[id_sender] = MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES

    def case_STATUS_FREE(self, id_sender):
        self.robot.known_robots[id_sender] = MESSAGE_TYPE_PRIORITY.STATUS_FREE

    def case_STOP(self):
        # TODO: Implement handling of STOP message
        pass

    def case_GO_TO_COORDINATES(self, id_sender, payload):
        # TODO: Implement handling of GO_TO_COORDINATES message
        pass

    def case_REPORT_BEGIN_ROLLCALL(self, id_sender, payload):
        if id_sender not in self.robot.known_robots:
            self.robot.known_robots[id_sender] = payload
        if self.robot.is_callrolling:
            self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.REPORT_END_ROLLCALL, ""))
            self.robot.is_callrolling = False

    def case_REPORT_END_ROLLCALL(self):
        if self.robot.is_callrolling:
            self.robot.is_callrolling = False

    def case_REPORT_BEGIN_ROLLCALL_AND_FREE(self, id_sender, payload):
        # TODO: Implement handling of REPORT_BEGIN_ROLLCALL_AND_FREE message
        pass
