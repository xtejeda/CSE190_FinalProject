#!/usr/bin/env python

#robot.py implementation goes here

import rospy
import math
import numpy

from cse_190_assi_3.msg import AStarPath, PolicyList
from read_config import read_config
from std_msgs.msg import Bool, String

from astar import *
from mdp import *

class Robot():
	def __init__(self):

		# Configure Variables
		self.config = read_config()
		rospy.init_node('robot')
		self.move_list = self.config["move_list"]
		self.map_size = self.config["map_size"]
		self.start = self.config["start"]
		self.goal = self.config["goal"]
		self.walls = self.config["walls"]
		self.pits = self.config["pits"]

		# Configure Publishers
		self.astar_pub = rospy.Publisher(
			"/results/path_list",
			AStarPath,
			queue_size = 100		
		)
		
		self.mdp_pub = rospy.Publisher(
			"/results/policy_list",
			PolicyList,
			queue_size = 100
		)
		
		self.done_pub = rospy.Publisher(
			"/map_node/sim_complete",
			Bool,
			queue_size = 10
		)
		
		self.arduino_pub = rospy.Publisher(
			"/results/arduino",
			String,
			queue_size = 10
		)
		rospy.sleep(1)
		
		# A* Search		
		astarResult = astarAlgorithm(self.move_list,
			self.start,self.goal,self.walls,self.pits, self.map_size)
		
		for i in range(0, len(astarResult)):
			self.astar_pub.publish(astarResult[i])
			
			# START
			if(i == 0):
				self.arduino_pub.publish("S")
				rospy.sleep(3)	
				continue		

			astarXY = astarResult[i]
			astarPrev = astarResult[i-1]			
			
			# RIGHT
			if(astarXY[0] == astarPrev[0] + 1 and astarXY[1] == astarPrev[1] + 0):
				self.arduino_pub.publish("R")
				rospy.sleep(3)
				continue

			# LEFT
			if(astarXY[0] == astarPrev[0] - 1 and astarXY[1] == astarPrev[1] + 0):
				self.arduino_pub.publish("L")
				rospy.sleep(3)
				continue

			# DOWN
			if(astarXY[0] == astarPrev[0] + 0 and astarXY[1] == astarPrev[1] + 1):
				self.arduino_pub.publish("D")
				rospy.sleep(3)
				continue

			# UP
			if(astarXY[0] == astarPrev[0] + 0 and astarXY[1] == astarPrev[1] - 1):
				self.arduino_pub.publish("U")
				rospy.sleep(3)
				continue
			rospy.sleep(1)
		rospy.sleep(1)
		# COMPLETE 		
		self.arduino_pub.publish("C")
		rospy.sleep(3)
			
		
		# MDP Search
		mdpResult = mdpAlgorithm(self.move_list,
			self.start,self.goal,self.walls,self.pits, self.map_size)
		self.mdp_pub.publish(mdpResult)
		rospy.sleep(3)
		

		#Shut down your robot node using rospy.signal_shutdown()
		self.done_pub.publish(True)
		rospy.sleep(3)
		rospy.signal_shutdown(0)
		rospy.spin()

if __name__ == '__main__':
	Robot()
