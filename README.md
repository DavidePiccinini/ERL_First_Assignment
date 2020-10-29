# Experimental Robotics Laboratory First Assignment
This assignment consists in developing a simple software architecture to simulate the behaviour of a robot moving in a 2D plane. 
The robot features three possible behaviours, i.e. Normal, Sleep and Play, and responds to user commands.

## System Architecture

### Component Diagram

<p align="center"> 
<img src="https://github.com/DavidePiccinini/ERL_First_Assignment/blob/master/diagrams/Component_Diagram.png?raw=true">
</p>

The software architecture is based on **three main components**:

- **Person module**

    This module mimics the behaviour of a person that controls the robot via voice commands and by pointing gestures. 


    It features two pub/sub interfaces to communicate with the finite state machine component: one sends strings containing voice commands on the *"voice_command"* topic and the other one two integers defining a location on the *"pointing_gesture"* topic.

- **Finite state machine**

    This component implements a finite state machine using "Smach".

    The three states, together with the transitions between them, will be further explained in the following paragraph.

- **Robot control service**

    This component implements a server/client pattern and checks the consistency of the requested location with respect to the map's boundaries.
    Each state of the finite state machine calls this service to move the robot to a certain location.

### State Diagram

<p align="center"> 
<img src="https://github.com/DavidePiccinini/ERL_First_Assignment/blob/master/diagrams/State_Diagram.png?raw=true">
</p>

This is the state diagram that shows how the finite state machine works:

When the robot is in **Normal** state it simply moves randomly by calling the robot control service to go to a valid location, i.e. inside the map boundaries.
The state transitions to *Sleep* when the sleep counter goes above a defined threshold, which means that the robot has reached a certain number of locations.
The state transitions to *Play* when the robot receives a "play" voice command from the user. 

When the robot is in **Sleep** state, it first reaches the predefined "Home" location, then stays there for some time and finally wakes up, transitioning back to the *Normal* state.

When the robot is in **Play** state, it first reaches the user and then waits for him/her to point a location: when done, it reaches the pointed location and then comes back to the user only to wait for other gestures.
The state automatically transitions back to *Normal* after some time has passed.

## ROS messages and parameters

Custom ROS **messages** are:

- **Location.msg**

    ```
    int64 x
    int64 y
    ```

    Defines a location in the 2D environment by using two integers: it's used in the pub/sub interface for the *"pointing_gesture"* topic.

- **VoiceCommand.msg**

    ```
    string command
    ```

    Defines a voice command that the user can send to the robot: it's used in the pub/sub interface for the *"voice_command"* topic.

- **MoveRobot.srv**

    ```
    int64 x
    int64 y
    ---
    bool goalReached
    ```

    Defines the request/response for the robot control server: the two integers define the location the robot has to move to and the bool tells whether the robot was able to reach its goal or not.

Custom ROS **parameters** are:

- `map/xmax` and `map/ymax`

    Define the map's boundaries: the map will be a rectangle with sides defined by these two parameters.

- `person/x` and `person/y`

    Define the position of the person in the 2D plane.

- `home/x` and `home/y`

    Define the position of the key location "Home".

- `time_scale`

    Defines the speed at which the simulation goes: e.g. a value of 2 means 2x speed.

- `robot/state`

    Defines the state which the robot is currently in.

## Packages and file list

Going in alphabetical order: