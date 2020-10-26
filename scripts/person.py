#!/usr/bin/env python

import rospy
import time
import random
from erl_first_assignment.msg import Location, VoiceCommand

def person():
    # Voice command publisher initialization
    pub1 = rospy.Publisher('voice_command', VoiceCommand, queue_size=1)

    # Pointing gesture publisher initialization
    pub2 = rospy.Publisher('pointing_gesture', Location, queue_size=1)

    # Initialize the person node
    rospy.init_node('person', anonymous=True)

    while not rospy.is_shutdown():
        rospy.loginfo('Loop.\n')

        # Publish a voice command
        # rospy.loginfo('Sending voice command.\n')
        com = VoiceCommand()
        com.command = 'play'
        pub1.publish(com)
        time.sleep(3)

        # Publish a location
        # rospy.loginfo('Sending pointing gesture.\n')
        '''
        loc = Location()
        loc.x = 1
        loc.y = 1
        pub2.publish(loc)
        time.sleep(3)
        '''

if __name__ == "__main__":
    try:
        person()
    except rospy.ROSInterruptException:
        pass