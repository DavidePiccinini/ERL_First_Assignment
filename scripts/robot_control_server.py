#!/usr/bin/env python

from __future__ import print_function

from erl_first_assignment.srv import MoveRobot, MoveRobotResponse
import rospy
import time
import random

##
# Checks if the requested position is inside the map boundaries
# @param x The x position of the location
# @param y The y position of the location
# @return  The consistency of the location with respect to the map
def checkConsistency(x, y):

    # Get the map's xmax and ymax
    xmax = rospy.get_param("map/xmax")
    ymax = rospy.get_param("map/ymax")

    if x >= 0 and x <= xmax and y >= 0 and y <= ymax:
        
        print('Robot control: Requested location is valid.\n')
        return True
    else:

        print('Robot control: Requested location is invalid.\n')
        return False

    #print("Requested location is valid.\n")
    #return True

##
# Callback function for the service
# @param req The client's requested location
# @return    Whether the robot was able to reach the destination or not
def moveToDestination(req):

    # Check consistency of the requested location
    isConsistent = checkConsistency(req.x, req.y)

    if isConsistent:
        # Sleep for a random amount of time and then notify that the 
        # destination has been reached

        # sleepTime = random.randint(2, 8)
        sleepTime = 5
        time.sleep(sleepTime)
        
        print('Robot control: The robot reached destination (%d, %d).\n'%(req.x, req.y))
        return MoveRobotResponse(True)
    else:
        return MoveRobotResponse(False)

##
# Client initialization
def robotControlServer():

    rospy.init_node('robot_control')
    s = rospy.Service('robot_control', MoveRobot, moveToDestination)
    print('Robot control: The robot is ready to receive commands.\n')
    rospy.spin()

if __name__ == "__main__":
    robotControlServer()