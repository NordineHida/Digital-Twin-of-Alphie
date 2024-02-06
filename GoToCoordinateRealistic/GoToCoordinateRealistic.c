/*
 * File:          GoToCoordinateRealistic.c
 * Date:          February 2024
 * Description:   The robot will turn on itself until it is facing the indicated coordinates, then it will move forward until it reaches the goal.
 * Author:        Nordine HIDA
 * Modifications:
 */


#define _BOOL_DEFINED

 /*
  * You may need to add include files like <webots/distance_sensor.h> or
  * <webots/motor.h>, etc.
  */
#include <webots/robot.h>
#include "MovementManager.h"
#include "PositioningManager.h"

  /*
   * You may want to add macros here.
   */
   //#define TIME_STEP 64

   //Time step of the simulation
int TIME_STEP;

/*
* Initialise attributs and robot settings
*/
void Initialisation()
{
    TIME_STEP = GetTimeStep();
    //init motors of the MovementManager
    MoveInit();
}

/*
 * This is the main program.
 * The arguments of the main function can be specified by the
 * "controllerArgs" field of the Robot node
 */
int main(int argc, char** argv) {
    /* necessary to initialize webots stuff */
    wb_robot_init();
    Initialisation();
    bool targetAchieved = false;

    //Coordinates goal
    Coordinates targetPosition = { 2.0, 2.0 };

    // Tolerance for isArrived
    double arrivalTolerance = 0.01;  // Adjust the tolerance as needed
    // Tolerance to get the right angle
    double angleTolerance = 3.0;

    //Declaration of WbDeviceTag variables for storing
    WbDeviceTag compass = wb_robot_get_device("compass");;
    WbDeviceTag gps = wb_robot_get_device("gps");
    wb_gps_enable(gps, 10);
    wb_compass_enable(compass, 10);


    /* main loop */
    while (wb_robot_step(TIME_STEP) != -1 && !targetAchieved)
    {
        // Get current position
        Coordinates currentPosition = GetPosition(gps);

        // Check if the robot has arrived at the target position
        if (!isArrived(currentPosition, targetPosition, arrivalTolerance))
        {

            // Get the bearing angle to the target coordinates
            double angleToDestination = GetBearingToCoordinate(currentPosition, targetPosition);

            double angleHeadingRobot = GetHeadingRobot(compass);

            // Rotate the robot until it faces the target coordinates
            RotateToDestination(compass, angleToDestination, angleTolerance);


            // Move forward
            MoveForward();
        }
        else
        {
            // Stop the robot when the target position is reached
            MoveStop();
            printf("Target position reached!\n");

            //Leaving the main loop
            targetAchieved = true;
        }
    }

    /* Enter your cleanup code here */

    /* This is necessary to cleanup webots resources */
    wb_robot_cleanup();

    return 0;
}
