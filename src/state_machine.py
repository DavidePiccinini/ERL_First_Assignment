#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random

# Define state Normal
class Normal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['sleep','play'])

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

    def execute(self, userdata):
        time.sleep(2)
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
    rospy.init_node('Robot_Behaviour')

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