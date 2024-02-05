/*
 * File:          PositioningManager.c
 * Date:          February 2024
 * Description:   Manage the position and the orientation of the track robot. It allows you to rotate to coordinates.             
 * Author:        Nordine HIDA
 * Modifications:
 */


#include "MovementManager.h"
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
 * Get the bearing angle in degrees to reach a specific coordinate.
 *
 * @param Coordinates robotPosition The current position coordinates of the robot
 * @param Coordinates targetCoordinates The target coordinates
 *
 * @return double The bearing angle in degrees
 */
double GetBearingToCoordinate(Coordinates robotPosition, Coordinates targetCoordinates)
{
    // Calculate angle to the target coordinates in radians
    double rad = atan2(targetCoordinates.y - robotPosition.y, targetCoordinates.x - robotPosition.x);

    // Convert angle to degrees
    double bearing = rad * 180.0 / M_PI;

    // Ensure the angle is in the range [0, 360]
    if (bearing < 0.0)
        bearing += 360.0;

    return bearing;
}

/*
 * Get the heading angle of the robot based on compass readings.
 *
 * @param WbDeviceTag compassTag The compass's tag of the robot
 * @return double The heading angle in degrees
 */
double GetHeadingRobot(WbDeviceTag compassTag)
{
    // Get current compass values
    const double* compassValues = wb_compass_get_values(compassTag);

    // Calculate heading angle in radians
    double rad = atan2(compassValues[0], compassValues[1]);

    // Convert angle to degrees
    double headingAngleDegrees = rad * 180.0 / M_PI;

    // Adjust angle to be in the range [0, 360)
    if (headingAngleDegrees < 0.0)
        headingAngleDegrees += 360.0;

    // Rotate the angle to have 0 degrees at north and 90 degrees at east
    headingAngleDegrees = 90.0 - headingAngleDegrees;

    // Adjust angle again to be in the range [0, 360)
    if (headingAngleDegrees < 0.0)
        headingAngleDegrees += 360.0;

    return headingAngleDegrees +180-270 ;
}





/*
 * Rotate the robot until it reaches the specified angle.
 *
 * @param WbDeviceTag compassTag The compass's tag of the robot
 * @param double angleToDestination The angle to the destination coordinates in degrees
 * @param double tolerance The tolerance to consider the destination reached
 */
void RotateToDestination(WbDeviceTag compassTag, double angleToDestination, double tolerance)
{
    // Get the heading angle (where is looking) the robot
    double headingRobotAngle = GetHeadingRobot(compassTag);

    // Calculate the angle difference between the robot's heading and the destination angle
    double angleDifference = angleToDestination - headingRobotAngle;

    // Adjust angle difference to be in the range [-180, 180)
    if (angleDifference < -180.0)
        angleDifference += 360.0;
    else if (angleDifference >= 180.0)
        angleDifference -= 360.0;

    printf("angle angleToDestination %f\n", angleToDestination);
    printf("headingRobotAngle %f\n", headingRobotAngle);
    printf("angle differnec %f\n \n \n", angleDifference);

    // Check tolerance to consider the destination reached
    if (!(fabs(angleDifference) < tolerance))
    {
        // Choose rotation direction based on the angle difference
        if (angleDifference < 0)
            MoveRight();  // Rotate right
        else
            MoveLeft();   // Rotate left

        // Update the simulation
        wb_robot_step(TIME_STEP);
        RotateToDestination(compassTag, angleToDestination, tolerance);  // Recursive call to continue rotation
    }
    else
    {
        printf("Angle reached!\n");
        MoveForward();  // Move to the destination
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
 * Check if the robot has arrived at the target coordinates with a tolerance
 *
 * @param Coordinates current The current coordinates of the robot
 * @param Coordinates target The target coordinates
 * @param double tolerance The tolerance value for both X and Y coordinates
 * 
 * @return true if the robot has arrived, false otherwise
 */
bool isArrived(Coordinates current, Coordinates target, double tolerance)
{
    double differenceX = fabs(current.x - target.x);
    double differenceY = fabs(current.y - target.y);

    return (differenceX < tolerance) && (differenceY < tolerance);
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