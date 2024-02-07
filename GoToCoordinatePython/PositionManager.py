import math
from webots import Robot
from MovementManager import MovementManager



# Structure pour stocker les coordonnées
class Coordinates:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class PositionManager:
    """
    Manage the position and the orientation of the track robot.
    It allows you to rotate to coordinates.
    """
    def __init__(self,robot):
        """
        Initialize PositionManager.

        Parameters:
            robot (Robot): The Robot instance.
        """
        self.robot = robot
        self.gps = self.robot.getDevice("gps")
        self.gps.enable(int(self.robot.getBasicTimeStep()))
        self.compass = self.robot.getDevice("compass")
        self.compass.enable(int(self.robot.getBasicTimeStep()))
        self.movement_manager = MovementManager(robot)
        self.time_step = -1

    def get_time_step(self):
        """
        Get the simulator time step.

        Returns:
            int: The time step of the simulation.
        """
        if self.time_step == -1:
            self.time_step = int(self.robot.getBasicTimeStep())
        return self.time_step

    def get_bearing_to_coordinate(self, robot_position, target_coordinates):
        """
        Get the bearing angle in degrees to reach a specific coordinate.

        Args:
            robot_position (Coordinates): The current position coordinates of the robot.
            target_coordinates (Coordinates): The target coordinates.

        Returns:
            double: The bearing angle in degrees.
        """
        rad = math.atan2(target_coordinates.y - robot_position.y, target_coordinates.x - robot_position.x)
        bearing = math.degrees(rad)
        if bearing < 0.0:
            bearing += 360.0
        return bearing

    def get_heading_robot(self):
        """
        Get the heading angle of the robot based on compass readings.

        Returns:
            double: The heading angle in degrees.
        """
        compass_values = self.compass.getValues()
        rad = math.atan2(compass_values[0], compass_values[2])
        heading_angle_degrees = math.degrees(rad)
        if heading_angle_degrees < 0.0:
            heading_angle_degrees += 360.0
        return heading_angle_degrees

    def rotate_to_destination(self, angle_to_destination, tolerance):
        """
        Rotate the robot until it reaches the specified angle.

        Args:
            angle_to_destination (double): The angle to the destination coordinates in degrees.
            tolerance (double): The tolerance to consider the destination reached.
        """
        heading_robot_angle = self.get_heading_robot()
        angle_difference = angle_to_destination - heading_robot_angle
        if angle_difference < -180.0:
            angle_difference += 360.0
        elif angle_difference >= 180.0:
            angle_difference -= 360.0

        if not abs(angle_difference) < tolerance:
            if angle_difference < 0:
                self.movement_manager.move_right()
            else:
                self.movement_manager.move_left()

            self.robot.step(self.get_time_step())
            self.rotate_to_destination(angle_to_destination, tolerance)
        else:
            print("Angle reached!")
            self.movement_manager.move_forward()
            self.robot.step(self.get_time_step())

    def get_position(self):
        """
        Get the position of the robot.

        Returns:
            Coordinates: The coordinates of the robot.
        """
        gps_values = self.gps.getValues()
        return Coordinates(gps_values[0], gps_values[2])

    def is_arrived(self, current, target, tolerance):
        """
        Check if the robot has arrived at the target coordinates with a tolerance.

        Args:
            current (Coordinates): The current coordinates of the robot.
            target (Coordinates): The target coordinates.
            tolerance (double): The tolerance value for both X and Y coordinates.

        Returns:
            bool: True if the robot has arrived, False otherwise.
        """
        difference_x = abs(current.x - target.x)
        difference_y = abs(current.y - target.y)
        return difference_x < tolerance and difference_y < tolerance

    def calculate_go_to(self, actual, target):
        """
        Calculate the vector to go from the current position to the target position.

        Args:
            actual (Coordinates): The current coordinates of the robot.
            target (Coordinates): The target coordinates.

        Returns:
            Coordinates: The vector to go to the target.
        """
        return Coordinates(target.x - actual.x, target.y - actual.y)
