#!/usr/bin/env python

import rospy
import time
import random
from erl_first_assignment.msg import Location, VoiceCommand

##
# Mimics the behaviour of a person controlling the robot.
# Sends either a voice command or points a location depending on the robot state.
def person():

    # Voice command publisher 
    pub1 = rospy.Publisher('voice_command', VoiceCommand, queue_size=1)

    # Pointing gesture publisher
    pub2 = rospy.Publisher('pointing_gesture', Location, queue_size=1)

    # Initialize the node
    rospy.init_node('person', anonymous=True)

    while not rospy.is_shutdown():

        # Retrieve the robot state
        robotState = rospy.get_param("robot/state")

        # Logic for sending the commands
        if robotState == 'normal':
            '''
            time.sleep(20)

            # Send the play voice command
            com = VoiceCommand()
            com.command = 'play'

            print('Person: Sending voice command: play.\n')
            pub1.publish(com)

            time.sleep(5)
            '''
            pass
        elif robotState == 'play':
            '''
            time.sleep(10)

            # Point a location
            loc = Location()
            loc.x = 1
            loc.y = 1

            print('Person: Pointing location (%d, %d).\n'%(loc.x, loc.y))
            pub2.publish(loc)

            time.sleep(5)
            pass
            '''
        else:
            print("Person: I'm letting the robot sleep peacefully.\n")
            time.sleep(5)
            pass

if __name__ == "__main__":
    try:
        person()
    except rospy.ROSInterruptException:
        pass