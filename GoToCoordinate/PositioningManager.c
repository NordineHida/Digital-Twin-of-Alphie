/*
 * File:          PositioningManager.c
 * Date:          February 2024
 * Description:   Manage the position and the orientation of the track robot. It allows you to rotate to coordinates.             
 * Author:        Nordine HIDA
 * Modifications:
 */


#include "MovementManager.c"
#include <stdbool.h>

//Webots library
#include <webots/compass.h>
#include <webots/gps.h>
#include <webots/robot.h>

//to get the Pi value with the standard lib (M_PI) and mathematical operations (atan2...)
#define _USE_MATH_DEFINES
#include <math.h>


//Time step of the simulation
int TIME_STEP;

// Structure of coordinates 
typedef struct {
    double x;
    double y;
} Coordinates;

/*
Method to get simulator time step.
Webots have simulator time step.
The basic time step is the time step increment used by Webots to advance the virtual time and perform physics simulation.
*/
int GetTimeStep()
{
    TIME_STEP = -1;
    if (TIME_STEP == -1)
        TIME_STEP = (int)wb_robot_get_basic_time_step();
    return TIME_STEP;
}

/*
* Get the bearing angle in degrees to 
* @param char compassTag The compass's tag of the robot
* @return double the angle to the coordinate in degrees
* 
* TODO AJOUTER COORDONNEE POUR AVOIR LE BEARING VERS LES COO EN INPUT
*/ 
double getBearingInDegrees(WbDeviceTag compassTag)
{
    const double* north = wb_compass_get_values(compassTag);
    double rad = atan2(north[1], north[0]);
    double bearing = (rad - 1.5708) / M_PI * 180.0;
    if (bearing < 0.0)
        bearing += 360.0;
    //printf("Angle du cap de la boussole : %f \n", bearing);
    return bearing;
}

/*
* Rotate the robot until it reaches the X, Y coordinate
*
* @param WbDeviceTag compassTag
* @param Coordinates destination The destination coordinates
*/
void RotateToDestination(WbDeviceTag compassTag, Coordinates destination)
{
    const double tolerance = 1;  // Tolerance to consider the destination reached

    // Get current compass values
    const double* compassValues = wb_compass_get_values(compassTag);

    // Calculate current compass angle in radians
    double currentAngleRad = atan2(compassValues[1], compassValues[0]);

    // Calculate angle to destination in radians
    double angleToDestinationRad = atan2(destination.y, destination.x);

    // Calculate angle difference in radians
    double angleDifferenceRad = angleToDestinationRad - currentAngleRad;

    // Adjust angle difference to be in the range [-π, π)
    if (angleDifferenceRad < -M_PI)
        angleDifferenceRad += 2.0 * M_PI;
    else if (angleDifferenceRad >= M_PI)
        angleDifferenceRad -= 2.0 * M_PI;

    // Convert angle to degrees
    double angleToDestination = angleDifferenceRad * 180.0 / M_PI;

    // Check tolerance to consider the destination reached
    if (!(fabs(angleToDestination) < tolerance))
    {
        // Choose rotation direction based on the angle difference
        if (angleToDestination > 0) 
            MoveLeft();  // Rotate left
        else 
            MoveRight();  // Rotate right

        // Update the simulation
        wb_robot_step(TIME_STEP);
        RotateToDestination(compassTag, destination);  // Recursive call to continue rotation
    }
    else
    {
        printf("Angle reached!\n");
        wb_robot_step(TIME_STEP);
    }
}


/*
* Get the position of the robot
* 
* @param WbDeviceTag gpsTag The GPS's tag
* @return Coordinates of the robot
*/
Coordinates GetPosition(WbDeviceTag gpsTag)
{
    Coordinates position;
    const double* gpsValues = wb_gps_get_values(gpsTag);
    position.x = gpsValues[0];
    position.y = gpsValues[1];
    return position;
}

/*
* Check if the robot has arrived at the target coordinates
*
* @param Coordinates current The current coordinates of the robot
* @param Coordinates target The target coordinates
* @return true if the robot has arrived, false otherwise
*/
bool isArrived(Coordinates current, Coordinates target) 
{
    double tolerance = 0.5;
    double differenceX = fabs(current.x - target.x);
    double differenceY = fabs(current.y - target.y);

    bool result = differenceX < tolerance && differenceY < tolerance;

    return result;
}

/*
* Calculate the vector to go from the current position to the target position
*
* @param Coordinates actual The current coordinates of the robot
* @param Coordinates target The target coordinates
* 
* @return Coordinates representing the vector to go to the target
*/
Coordinates CalculateGoTo(Coordinates actual, Coordinates target) 
{
    Coordinates goTo;
    goTo.x = target.x - actual.x;
    goTo.y = target.y - actual.y;
    return goTo;
}