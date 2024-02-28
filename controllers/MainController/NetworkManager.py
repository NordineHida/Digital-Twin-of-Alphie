"""
File:           NetworkManagerRemote.py
Date:           February 2024
Description:    Manage the network of communication between robots,
                facilitating the retrieval of nearby robots and
                determining which ones should take action.
Author:         Nordine HIDA
Modifications:
"""

from MovementManager import *
from CommunicationManager import *


class NetworkManager:
    """
    Manage the network of communication between robots,
    facilitating the retrieval of nearby robots and
    determining which ones should take action.
    """

    def __init__(self, robot: RobotUp):
        """
        Initialize the NetworkManager.

        Args:
            robot (RobotUp): The robot
        """
        self.robot = robot
        self.robot_name = self.robot.getName()

        # Communication manager
        self.communication = CommunicationManager(self.robot)
        self.is_stopped = False

    def go_to_coordinates(self, x: float, y: float):
        """
        If the robot is free, call the task to move the robot to coordinates
        else it adds those coordinates to its list of next coordinates

        When it reaches its goal, it sends a message to tell that it is free and where it stopped.
        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        """
        import Task_GoToCoordinates as GTC

        # if i'm free I move
        if self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
            self.robot.robot_current_task = str(MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES)
            GTC.go_to_coordinates(self.robot, Coordinates(float(x), float(y)))
            self.robot.robot_current_task = MESSAGE_TYPE_PRIORITY.STATUS_FREE
            self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.STATUS_FREE, f"{MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES}:{x}:{y}"))

        # if I'm already moving, I add new Coordinates to move
        elif self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES:
            self.robot.next_coordinates.append(Coordinates(float(x), float(y)))

    def case_REPORT_STATUS(self, id_sender: str, payload: str):
        """
        Handle the REPORT_STATUS message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        # TODO: Handle the REPORT_STATUS message
        pass

    def case_REPORT_POSITION(self, id_sender: str, payload: str):
        """
        Handle the REPORT_POSITION message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        # TODO: Handle the REPORT_POSITION message
        pass

    def case_STATUS_GOTOCOORDINATES(self, id_sender: str, payload: str):
        """
        Handle the STATUS_GOTOCOORDINATES message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        # TODO: Handle the STATUS_GOTOCOORDINATES message
        pass

    def case_STATUS_FREE(self, id_sender: str, payload: str):
        """
        Handle the STATUS_FREE message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        self.robot.known_robots[id_sender] = MESSAGE_TYPE_PRIORITY.STATUS_FREE
        # if the previous robot tell's that it is free right after a GoToCoordinates task, I follow it
        if id_sender == self.robot.prev_rob and payload.startswith(str(MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES)):
            msg, x, y = payload.split(":")
            if self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                self.go_to_coordinates(float(x), float(y))
            else:
                self.robot.next_coordinates.append(Coordinates(float(x), float(y)))

        elif self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES:
            if payload == self.robot.robot_current_task:
                # TODO LE PAYLOAD EST AVEC DES FLOAT DONC DES X.0 DONC FAUT ADAPTER LE ==
                self.case_STOP(id_sender, payload)
                print("il ma doublé j'y vais pas")

        elif id_sender == self.robot.prev_rob and payload == "STOP":
            self.case_STOP(id_sender, payload)

    def case_STOP(self, id_sender: str, payload: str):
        """
        Handle the STOP message.

        Clear all messages and coordinates in the robot's memory
        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        movement = MovementManager(self.robot)
        movement.stop()
        self.robot.robot_current_task = MESSAGE_TYPE_PRIORITY.STATUS_FREE
        self.communication.clear_messages()
        self.robot.next_coordinates.clear()
        # if I have a next I send a stop message
        if self.robot.next_rob:
            self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.STATUS_FREE, "STOP"))
        self.is_stopped = True

    def case_GO_TO_COORDINATES(self, id_sender: str, payload: str):
        """
        Handle the GO_TO_COORDINATES message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        x, y = payload.split(":")
        if not self.robot.prev_rob:
            if self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                self.go_to_coordinates(float(x), float(y))
            else:
                self.robot.next_coordinates.append(Coordinates(float(x), float(y)))

    def case_REPORT_BEGIN_ROLLCALL(self, id_sender: str, payload: str):
        """
        Handle the REPORT_BEGIN_ROLLCALL message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        if not self.robot.is_callrolling and id_sender not in self.robot.known_robots:
            self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL,
                                                    str(self.robot.robot_current_task)))
            self.robot.is_callrolling = True

        if id_sender not in self.robot.known_robots:
            if id_sender != "Remote":
                self.robot.known_robots[id_sender] = payload

    def case_REPORT_END_ROLLCALL(self):
        """
        Handle the REPORT_END_ROLLCALL message.

        """
        if self.robot.is_callrolling:
            self.robot.is_callrolling = False
            self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.REPORT_END_ROLLCALL, ""))

    def update(self) -> int:
        """
        Handle the received message.

        Returns:
            int : case that was executed (-1 if no messages was handled)
        """
        case_executed = -1

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

            case_executed = message_type.value

            match message_type:
                case MESSAGE_TYPE_PRIORITY.REPORT_STATUS:
                    self.case_REPORT_STATUS(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_POSITION:
                    self.case_REPORT_POSITION(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES:
                    self.case_STATUS_GOTOCOORDINATES(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                    self.case_STATUS_FREE(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STOP:
                    self.case_STOP(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES:
                    self.case_GO_TO_COORDINATES(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL:
                    self.case_REPORT_BEGIN_ROLLCALL(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_END_ROLLCALL:
                    self.case_REPORT_END_ROLLCALL()

                case MESSAGE_TYPE_PRIORITY.REPORT_END_ROLLCALL:
                    self.case_REPORT_END_ROLLCALL()

                case _:
                    print("Unknown message received")
                    pass

        if self.robot.next_coordinates and self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
            x = self.robot.next_coordinates[0].x
            y = self.robot.next_coordinates[0].y
            self.robot.next_coordinates.pop(0)
            self.go_to_coordinates(x, y)

        self.update_prev_next_robot()
        return case_executed

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
