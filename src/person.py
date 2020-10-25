#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from erl_first_assignment.msg import Location

def person():
    # Voice command publisher initialization
    pub1 = rospy.Publisher('voice_command', String)
    rospy.init_node('personVoiceCommand', anonymous=True)
    rate = rospy.Rate(1)

    # Pointing gesture publisher initialization
    # pub2 = rospy.Publisher('pointing_gesture', Location)
    # rospy.init_node('personPointingGesture', anonymous=True)
    # rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        rospy.loginfo('Loop.\n')
        # rospy.loginfo('Sending voice command.\n')
        # pub1.publish('play')
        # rate.sleep()

        # rospy.loginfo('Sending pointing gesture.\n')
        # pub2.publish('x, y')
        # rate.sleep()

if __name__ == "__main__":
    try:
        person()
    except rospy.ROSInterruptException:
        pass