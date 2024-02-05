/*
 * File:          GoToCoordinate.c
 * Date:          February 2024
 * Description:   The robot will turn on itself until it is facing the indicated coordinates, then it will move forward until it reaches the goal.
 * Author:        Nordine HIDA 
 * Modifications:
 */

/*
 * You may need to add include files like <webots/distance_sensor.h> or
 * <webots/motor.h>, etc.
 */
#include <webots/robot.h>
#include "PositioningManager.c"
#include "MovementManager.c"

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
int main(int argc, char **argv) {
    /* necessary to initialize webots stuff */
    wb_robot_init();
    Initialisation();

    //Coordinates goal
    Coordinates targetPosition = { 2.0, 2.0 };

    /*
     * You should declare here WbDeviceTag variables for storing
     * robot devices like this:
     *  WbDeviceTag my_sensor = wb_robot_get_device("my_sensor");
     *  WbDeviceTag my_actuator = wb_robot_get_device("my_actuator");
    */

    WbDeviceTag compass = wb_robot_get_device("compass");;
    WbDeviceTag gps = wb_robot_get_device("gps");
    wb_gps_enable(gps, 10);
    wb_compass_enable(compass, 10);
    
    // Tolerance for isArrived
    double arrivalTolerance = 1.0;  // Adjust the tolerance as needed

    /* main loop */
    while (wb_robot_step(TIME_STEP) != -1) 
    {
        // Get current position
        Coordinates currentPosition = GetPosition(gps);

        // Check if the robot has arrived at the target position
        if (!isArrived(currentPosition, targetPosition, arrivalTolerance)) 
        {
            // Calculate the vector to go from the current position to the target position
            Coordinates goToVector = CalculateGoTo(currentPosition, targetPosition);

            // Get the bearing angle to the target coordinates
            double angleToDestination = getBearingToCoordinate(compass, targetPosition);

            // Rotate the robot until it faces the target coordinates
            RotateToDestination(compass, targetPosition);

            // Move forward
            MoveForward();
        }
        else 
        {
            // Stop the robot when the target position is reached
            MoveStop();
            printf("Target position reached!\n");
        }
    }
    
    /* Enter your cleanup code here */
    
    /* This is necessary to cleanup webots resources */
    wb_robot_cleanup();
    
    return 0;
}
