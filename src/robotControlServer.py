#!/usr/bin/env python

from __future__ import print_function

from erl_first_assignment.srv import MoveRobot, MoveRobotResponse
import rospy
import time
import random

# Function to check if the requested position is valid
def checkConsistency(x, y):

    # Get the map's xmax and ymax
    xmax = rospy.get_param("/map/xmax")
    ymax = rospy.get_param("/map/ymax")

    if x >= 0 and x <= xmax and y >= 0 and y <= ymax:
        
        print("Requested location is valid.\n")
        return True
    else:

        print("Requested location is invalid.\n")
        return False

# Callback function
def moveToDestination(req):
    # Check consistency of the requested location
    isConsistent = checkConsistency(req.x, req.y)

    if isConsistent:
        # Sleep for a random amount of time and then notify that the 
        # destination has been reached

        # sleepTime = random.randint(2, 8)
        sleepTime = 1
        time.sleep(sleepTime)
        print("Reached destination (%s, %s).\n", req.x, req.y)
        return MoveRobotResponse(True)
    else:
        return MoveRobotResponse(False)

def robotControlServer():
    rospy.init_node('robot_control_server')
    s = rospy.Service('robot_control_server', MoveRobot, moveToDestination)
    print("The robot is ready to receive commands.\n")
    rospy.spin()

if __name__ == "__main__":
    robotControlServer()