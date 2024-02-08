#ifndef POSITIONING_MANAGER_H
#define POSITIONING_MANAGER_H

/*
 * File:          PositioningManager.h
 * Date:          February 2024
 * Description:   Header file for managing the position and orientation of the track robot.
 *                It allows you to rotate to coordinates.
 * Author:        Nordine HIDA
 * Modifications:
 */

#include <webots/compass.h>
#include <webots/gps.h>
#include <webots/robot.h>
#include <stdbool.h>

#include "MovementManager.h"

 // Structure for storing coordinates
typedef struct {
    double x;
    double y;
} Coordinates;

/*
 * Get the simulator time step.
 *
 * @return int The time step of the simulation
 */
int GetTimeStep();

/*
 * Get the bearing angle in degrees to reach a specific coordinate.
 *
 * @param Coordinates robotPosition The current position coordinates of the robot
 * @param Coordinates targetCoordinates The target coordinates
 *
 * @return double The bearing angle in degrees
 */
double GetBearingToCoordinate(Coordinates robotPosition, Coordinates targetCoordinates);

/*
 * Get the heading angle of the robot based on compass readings.
 *
 * @param WbDeviceTag compassTag The compass's tag of the robot
 * @return double The heading angle in degrees
 */
double GetHeadingRobot(WbDeviceTag compassTag);

/*
 * Rotate the robot until it reaches the specified angle.
 *
 * @param WbDeviceTag compassTag The compass's tag of the robot
 * @param double angleToDestination The angle to the destination coordinates in degrees
 * @param double tolerance The tolerance to consider the destination reached
 */
void RotateToDestination(WbDeviceTag compassTag, double angleToDestination, double tolerance);

/*
 * Get the position of the robot.
 *
 * @param WbDeviceTag gpsTag The GPS's tag
 * @return Coordinates The coordinates of the robot
 */
Coordinates GetPosition(WbDeviceTag gpsTag);

/*
 * Check if the robot has arrived at the target coordinates with a tolerance.
 *
 * @param Coordinates current The current coordinates of the robot
 * @param Coordinates target The target coordinates
 * @param double tolerance The tolerance value for both X and Y coordinates
 *
 * @return true if the robot has arrived, false otherwise
 */
bool isArrived(Coordinates current, Coordinates target, double tolerance);

/*
 * Calculate the vector to go from the current position to the target position.
 *
 * @param Coordinates actual The current coordinates of the robot
 * @param Coordinates target The target coordinates
 *
 * @return Coordinates The vector to go to the target
 */
Coordinates CalculateGoTo(Coordinates actual, Coordinates target);

#endif