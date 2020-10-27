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

##
# Calls the "robot_control" service
# @param x The x position of the destination
# @param y The y position of the destination
def robotControlCall(x, y):

    rospy.wait_for_service('robot_control')
    try:
        robot_control = rospy.ServiceProxy('robot_control', MoveRobot)
        response = robot_control(x, y)
        return response.goalReached
    except rospy.ServiceException as e:
        print("Service call failed %s.\n"%e)

## 
# Callback for the 'voice_command' topic
# @param data The voice command
def receivedVoiceCommand(data):

    rospy.loginfo("The NORMAL state received the command %s.\n"%data.command)

    # Change the robot state param
    rospy.set_param("robot/state", "play")

## 
# Callback for the 'pointing_gesture' topic
# @param data The pointed location
def receivedPointingGesture(data):

    rospy.loginfo("The PLAY state received the pointing gesture (%s, %s).\n"%(data.x, data.y))
    
    # Service call
    robotControlCall(data.x, data.y)

##
# Define Normal state
class Normal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['sleep','play'],
                                   input_keys=['sleep_counter_in'],
                                   output_keys=['sleep_counter_out'])

        rospy.Subscriber('voice_command', VoiceCommand, receivedVoiceCommand)
        self.threshold = 5

    def execute(self, userdata):

        time.sleep(5)
        rospy.set_param("robot/state", "normal")
        print('State machine: Executing state NORMAL.\n')
        sleepCounter = userdata.sleep_counter_in 

        while sleepCounter < self.threshold:
            robotControlCall(3, 3)
            sleepCounter+=1

        userdata.sleep_counter_out = sleepCounter
        return 'sleep'

##
# Define state Sleep
class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['wakeup'],
                                   output_keys=['sleep_counter_out'])

    def execute(self, userdata):
        
        time.sleep(5)
        rospy.set_param("robot/state", "sleep")
        print('State machine: Executing state SLEEP\n')

        # Retrieve "home" position
        homex = rospy.get_param("home/x")
        homey = rospy.get_param("home/y")

        # Call robot control service to go "home"
        robotControlCall(homex, homey)

        # Wait for x seconds
        time.sleep(10)

        # Go back to the normal state
        userdata.sleep_counter_out = 0
        return 'wakeup'

##
# Define state Play
class Play(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['stopplaying'],
                                   input_keys=['sleep_counter_in'],
                                   output_keys=['sleep_counter_out'])
        rospy.Subscriber('pointing_gesture', Location, receivedPointingGesture)

    def execute(self, userdata):
        time.sleep(4)
        rospy.set_param("robot/state", "play")
        print('State machine: Executing state PLAY\n')

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

##
# State machine initialization
def main():
    rospy.init_node('robot_behaviour', anonymous=True)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=[])
    sm.userdata.s_counter = 0

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('NORMAL', Normal(),
                                transitions={'sleep': 'SLEEP',
                                             'play': 'PLAY'},
                                remapping={'sleep_counter_in':'s_counter', 
                                           'sleep_counter_out':'s_counter'})
        smach.StateMachine.add('SLEEP', Sleep(),
                                transitions={'wakeup': 'NORMAL'},
                                remapping={'sleep_counter_out':'s_counter'})
        smach.StateMachine.add('PLAY', Play(),
                                transitions={'stopplaying': 'NORMAL'},
                                remapping={'sleep_counter_in':'s_counter', 
                                           'sleep_counter_out':'s_counter'})

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