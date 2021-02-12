#!/usr/bin/env python

import rospy
from moveit_commander.move_group import MoveGroupCommander
rospy.init_node('move_example')

rospy.loginfo("Waiting 15 sec before actually starting...")
rospy.sleep(15)
rospy.loginfo("Connecting to move group...")
commander = MoveGroupCommander("arm_and_finger")
rospy.loginfo("Connected!")

rate = rospy.Rate(1)
while not rospy.is_shutdown():
    rospy.loginfo("Going to zero...")
    commander.set_joint_value_target([0, 0, 0, 0, 0, 0])
    commander.go()
    rospy.loginfo("Going to a pose target...")
    commander.set_pose_target([0, 0, 0.25] + [1, 0, 0, 0])
    commander.go()
    rate.sleep(1)
