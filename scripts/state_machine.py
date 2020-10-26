#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
from std_msgs.msg import String
from erl_first_assignment.srv import MoveRobot
from erl_first_assignment.msg import Location, VoiceCommand

# Service call
def robotControlClient(x, y):
    rospy.wait_for_service('robot_control')
    try:
        robot_control = rospy.ServiceProxy('robot_control', MoveRobot)
        response = robot_control(x, y)
        return response.goalReached
    except rospy.ServiceException as e:
        print("Service call failed %s.\n"%e)

# Callback for the 'voice_command' topic
def receivedVoiceCommand(data):
    rospy.loginfo(rospy.get_caller_id() + "The NORMAL state received the command %s.\n", data.data)
    playState = True

# Callback for the 'pointing_gesture' topic
def receivedPointingGesture(data):
    rospy.loginfo(rospy.get_caller_id() + "The PLAY state received the pointing gesture (%s, %s).\n", data.data.x, data.data.y)
    # Service call

# Define state Normal
class Normal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['sleep','play'])
        rospy.Subscriber('voice_command', VoiceCommand, receivedVoiceCommand)

    def execute(self, userdata):
        time.sleep(2)
        rospy.loginfo('Executing state NORMAL\n')
        # While sleepcounter < threshold 
        #   if person issued a play command
        #       change state to play
        #   else
        #       call robot control service with a random location
        #       sleepcounter++
        #   
        #   sleepcounter = 0
        #   change state to sleep
        return 'sleep'

# Define state Sleep
class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['wakeup'])

    def execute(self, userdata):
        time.sleep(4)
        rospy.loginfo('Executing state SLEEP\n')
        # retrieve "home" position
        # call robot control service to go "home"
        # wait for x seconds
        # change state to normal
        return 'wakeup'

# Define state Play
class Play(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['stopplaying'])
        rospy.Subscriber('pointing_gesture', Location, receivedPointingGesture)

    def execute(self, userdata):
        time.sleep(4)
        rospy.loginfo('Executing state PLAY\n')
        # retrieve the person's position
        # call robot control service to go to the person's position
        # sleepcounter++
        # allow the person's gestures to be received
        # while gesturesPerformed < threshold1 and timePassed < threshold2
        #   if the user pointed a location
        #       call robot control service to go that location
        #       call robot control service to come back to the person's position
        #       sleepcounter++
        #       gesturesPerformed++
        #   timePassed++
        #   wait for x seconds
        # gesturesPerformed = 0
        # timePassed = 0
        # change state to normal
        return 'stopplaying'

# Main function
def main():
    rospy.init_node('Robot_Behaviour', anonymous=True)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=[])
    sm.userdata.s_counter = 0

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('NORMAL', Normal(),
                                transitions={'sleep': 'SLEEP',
                                             'play': 'PLAY'})
        smach.StateMachine.add('SLEEP', Sleep(),
                                transitions={'wakeup': 'NORMAL'})
        smach.StateMachine.add('PLAY', Play(),
                                transitions={'stopplaying': 'NORMAL'})

    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute SMACH plan
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == "__main__":
    main()