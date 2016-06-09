#!usr/bin/env python

import math
import numpy
import random

from read_config import read_config

def mdpAlgorithm(move_list, start, goal, walls, pits, map_size):
	
	# Configure Variables
	config = read_config()
	
	max_iterations = config["max_iterations"]
	threshold_difference = config["threshold_difference"]
	
	stepReward = config["reward_for_each_step"]
	wallReward = config["reward_for_hitting_wall"]
	goalReward = config["reward_for_reaching_goal"]
	pitReward = config["reward_for_falling_in_pit"]
	
	#initialize policy and reward map for return
	policyMap = [["-" for x in range(map_size[1])] for y in range (map_size[0])]
	rewardMap = [[stepReward for x in range(map_size[1])] for y in range (map_size[0])]
	
	# Set Goal	
	policyMap[goal[0]][goal[1]] = "GOAL"
	rewardMap[goal[0]][goal[1]] = goalReward
	
	# Set Walls & Pits	
	for w in range(0, len(walls)):
		wall = walls[w]
		policyMap[wall[0]][wall[1]] = "WALL"
		rewardMap[wall[0]][wall[1]] = wallReward
	for p in range(0, len(pits)):
		pit = pits[p]
		policyMap[pit[0]][pit[1]] = "PIT"
		rewardMap[pit[0]][pit[1]] = pitReward

	#used for max iteration check or threshold difference
	iterator = 0
	oldReward = 0
	newReward = 0

	flag = True
	neighbor = []
    
	# Move through each position on the map
	while(flag):
		for x in range(0, map_size[0]):
			for y in range(0, map_size[1]):
				position = [x, y]
				oldReward = rewardMap[x][y]
				if(position != goal):
					calculateUtility(position, move_list, map_size, pits, walls, rewardMap)
				newReward = rewardMap[x][y]
		threshold = numpy.sum(numpy.abs(oldReward - newReward))
		if (iterator == max_iterations or threshold <= threshold_difference):
			flag = False
		else:
			iterator += 1
    
	# Find optimal policy         
	for x in range(0, map_size[0]):
		for y in range(0, map_size[1]):
			position = [x, y]
			neighbor = getNeighbors(x, y, move_list, map_size)
			best, bestXY = bestNeighbor(neighbor, rewardMap)
			# Check if a wall			
			if (position in walls):
				continue
			# Check if a pit
			if(position in pits):
				continue
			# Check if goal	
			if (position != goal):
				policyMap[x][y] = direction(position, bestXY)

	mdpResult = [0 for i in range(0, len(policyMap)) * (len(policyMap[0]))]
	for i in range(0, len(policyMap)):
		for j in range(0, len(policyMap[0])):
			mdpResult[(len(policyMap[0])*i)+j] = policyMap[i][j]
 
	return mdpResult

# Create array of neighbors
def getNeighbors(x, y, move_list, map_size):

	neighbors = []

	for i in range(0, len(move_list)):
		# Grab move
		nextMove = move_list[i]
		neighborXY = [(x + nextMove[1]), (y + nextMove[0])]		
		if((neighborXY[1] < 0) 
			or (neighborXY[1] >= map_size[1])
			or (neighborXY[0] < 0)
			or (neighborXY[0] >= map_size[0])):
			neighbors.append(["-"])
		else:		
			neighbors.append(neighborXY)
	
	return neighbors

# Finds the neighbor with the highest reward
def bestNeighbor(neighbors, rewardMap):
	
	# Configure Neighbors
	downXY = neighbors[0]
	upXY = neighbors[1]
	rightXY = neighbors[2]
	leftXY = neighbors[3]

	# Initialize rewards
	rewards = []

	# Check is there is a reward for moving up
	if (upXY[0] != "-"):
		upReward = rewardMap[upXY[0]][upXY[1]]
	else:
		upReward = 0
	
	# Check is there is a reward for moving down
	if (downXY[0] != "-"):
		downReward = rewardMap[downXY[0]][downXY[1]]
	else:
		downReward = 0
	
	# Check is there is a reward for moving left
	if (leftXY[0] != "-"):
		leftReward = rewardMap[leftXY[0]][leftXY[1]]
	else:
		leftReward = 0
	
	# Check is there is a reward for moving right
	if(rightXY[0] != "-"):
		rightReward = rewardMap[rightXY[0]][rightXY[1]]
	else:
		rightReward = 0
   
	rewards.append(downReward)
	rewards.append(upReward)
	rewards.append(rightReward)
	rewards.append(leftReward)
	index = 0
	
	best = 0
	bestXY = []
	for i in range(0, len(rewards)):
		if(rewards[i] > best):
			best = rewards[i]
			index = i
	bestXY = neighbors[index]
	
	return best, bestXY

# Returns best direction
def direction(position1, position2):

	move = [position2[0]-position1[0], position2[1]-position1[1]]

	if(move == [-1, 0]):
		return "N"
	if(move == [1, 0]):
		return "S"
	if(move == [0, 1]):
		return "E"
	if(move == [0, -1]):
		return "W"

# Calculates the utility of a cell
def calculateUtility(position, move_list, map_size, pits, walls, rewardMap):
	
	# Intitialize Variables
	config = read_config()
	discount_factor = config["discount_factor"]
	
	prob_move_forward = config["prob_move_forward"]
	prob_move_backward = config["prob_move_backward"]
	prob_move_left = config["prob_move_left"]
	prob_move_right = config["prob_move_right"]
	
	generate_video = config["generate_video"]	    

	# Check if position is a pit or a wall
	if(position in pits):
		return
	if(position in walls):
		return

	neighbors = getNeighbors(position[0], position[1], move_list, map_size)
	forwardReward = 0
	forward = []
	neighborCount = 0

	for i in range(0, len(neighbors)):
		neighbor = neighbors[i]
		if(neighbor[0] != "-" and rewardMap[neighbor[0]][neighbor[1]] > forwardReward):
			forwardReward = rewardMap[neighbor[0]][neighbor[1]]
			forward = neighbor
			neighborCount = i
        
	if (forward != []):
		left, right = leftRightForward(neighborCount, forward)

		if (left[0] < 0
			or left[1] < 0 
			or left[0] >= map_size[0] 
			or left[1] >= map_size[1]):
			leftReward = 0
		else:
			leftReward = rewardMap[left[0]][left[1]]

		if (right[0] < 0 
			or right[1] < 0 
			or right[0] >= map_size[0] 
			or right[1] >= map_size[1]):
			rightReward = 0
		else:
			rightReward = rewardMap[right[0]][right[1]]
        
		rewardMap[position[0]][position[1]] = rewardMap[position[0]][position[1]] * discount_factor
		fReward = (prob_move_forward*forwardReward) 
		lReward = (prob_move_left*leftReward) 
		rReward = (prob_move_right*rightReward)
		rewardMap[position[0]][position[1]] += fReward + lReward + rReward

# return the left and right indicies relative to the forward
def leftRightForward(val, next):
	left = []
	right = []
	
	if (val == 0):
		left = [next[0]+1, next[1]-1]
		right = [next[0]+1, next[1]+1]
	elif (val == 1):
		left = [next[0]+1, next[1]-1]
		right = [next[0]-1, next[1]-1]
	elif (val == 2):
		left = [next[0]+1, next[1]+1]
		right = [next[0]+1, next[1]-1]
	elif (val == 3):
		left = [next[0]-1, next[1]-1]
		right = [next[0]+1, next[1]-1]
	
	return left, right
