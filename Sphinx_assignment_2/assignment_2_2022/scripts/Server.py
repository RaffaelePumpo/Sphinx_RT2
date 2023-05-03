#! /usr/bin/env python
"""
.. module:: Server
    :platform: Unix
    :synopsis: Python module to create the server node

.. moduleauthor:: *Raffaele Pumpo* S5457102@studenti.unige.it

This node creates the server and wait for the client to send the goal

Subscriber: 
/reaching_goal/result

Service:
 /goals
"""

import rospy
from geometry_msgs.msg import Point, Pose, Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from tf import transformations
from std_srvs.srv import *
import time
import sys
import select
from assignment_2_2022.srv import Goals, GoalsResponse



# Variables to count the number of goals reached and canceled
canceled = 0
reached = 0

status_canc = 2
status_reach = 3


def callback(msg):
    """
    Function to get the status of the goal and update the variables canceled and reached

    Args:
        msg (PlanningActionResult): message from reaching_goal/result topic with the status of the goal
    """

    global canceled, reached

    # Get the status 
    status = msg.status.status

    # Goal canceled
    if status == status_canc:
        canceled = canceled + 1

    # Goal reached
    elif status == status_reach:
        reached = reached + 1
		


def number_goals(req):
    """
     Function to give the number of goals reached and canceled

     Args:
        req (GoalsRequest): request from the client
     """

    return  GoalsResponse(reached, canceled)



def main():
    """
    Function to initialize the  node, create the subscriber and the service
    */reaching_goal/result* topic with the status of the goal
    */goals* service to give the number of goals reached and canceled
    """
    # Initialize the node
    rospy.init_node('server_node_b')
    
    # Subscriber
    sub = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, callback)
    
    # Service
    s = rospy.Service('/goals', Goals, number_goals)
    
    # Wait for the service to be called
    rospy.spin()
    
    

if __name__ == "__main__":
    main()
