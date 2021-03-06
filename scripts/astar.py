#!/usr/bin/env python
# astar implementation needs to go here

import math
import numpy

def astarAlgorithm(move_list, start, goal, walls, pits, map_size):
	
	# Initialize start node
	startNode = Node(0, start[0], start[1], 0, 0, 0)
	
	# Initialize unexplored & explored sets
	openSet = []
	openSet.append(startNode)	
	closedSet = []
	
	#Initialize path & cost
	currentPath = []
	currentPath.append(start)	
		
	# Search through unexplored set
	while(len(openSet) != 0):
		# Set position
		best = openSet[0].f
		for j in range (0, len(openSet)):
			if(openSet[j].f <= best):
				best = openSet[j].f
				currentPosition = openSet[j]
				bestVal = j
				
		openSet.remove(openSet[bestVal])
		currentXY = [currentPosition.x, currentPosition.y]	
		
		#print "Checking Node: [%s, %s]" % (currentXY[0], currentXY[1])
		
		# Check if goal is met
		if(currentXY == goal):
			currentPath.append(currentXY)
			#print "Found the goal!!"
			break
		
		# Check neighbors
		flag = False
		for i in range(0, len(move_list)):
			
			# Grab move
			nextMove = move_list[i]
			#print "        Checking move: [%s, %s]" % (nextMove[0], nextMove[1])

			# Initialize Neighbor
			neighborXY = [(currentXY[0] + nextMove[0]), (currentXY[1] + nextMove[1])]
			neighborG = currentPosition.g + 1
			neighborH = heuristic(goal, neighborXY)
			neighborF = neighborG + neighborH			
			neighbor = Node(currentPosition, neighborXY[0], neighborXY[1],
					neighborF, neighborG, neighborH)
			
			# Check if neighbor is on the map
			if((neighborXY[0] < 0) 
				or (neighborXY[0] >= map_size[0])
				or (neighborXY[1] < 0)
				or (neighborXY[1] >= map_size[1])):
				#print "        Off Map: [%s, %s]" % (neighborXY[0], neighborXY[1])
				continue

			# Check if neighbor was previously explored
			if(neighbor in closedSet):
				#print "        Repeat: [%s, %s]" % (neighborXY[0], neighborXY[1])
				continue

			# Check if neighbor is a wall
			if(neighborXY in walls):
				#print "        Wall: [%s, %s]" % (neighborXY[0], neighborXY[1])
				continue
			
			# Check if neighbor is a pit
			if(neighborXY in pits):
				#print "        Pit: [%s, %s]" % (neighborXY[0], neighborXY[1])
				continue
			
			# Check if neighbor is already in open list
			for i in range(0, len(openSet)):
				if(openSet[i].x == neighbor.x
					and openSet[i].y == neighbor.y
					and openSet[i].f < neighbor.f):
					flag = True
					#print "        OS: [%s, %s]" % (neighborXY[0], neighborXY[1])
					break

			# Check if neighbor is already in closed list
			for i in range(0, len(closedSet)):
				if(closedSet[i].x == neighbor.x 
					and closedSet[i].y == neighbor.y
					and closedSet[i].f < neighbor.f):
					flag = True
					#print "        CS: [%s, %s]" % (neighborXY[0], neighborXY[1])
					break
			if(flag):
				flag = False
				continue

			# Keep track of neighbor with the lowest cost
			openSet.append(neighbor)
			#print "        Added neighbor: [%s, %s]" % (neighborXY[0], neighborXY[1])
			
			
	
		# Add neighbor as best to search
		closedSet.append(currentPosition)
		
	# Loop back through parents
	n = currentPosition
	while n is not 0:
		n = n.parent
		if(n):
			currentPath.append([n.x, n.y])
	currentPath.reverse()	
	return currentPath

def heuristic(goal, position):
	#print "Running Heuristic..."
	return abs(goal[0] - position[0]) + abs(goal[1] - position[1])

class Node():
	def __init__(self, parent, x, y, f, g, h):
		self.parent = parent
		self.x = x
		self.y = y
		self.f = f
		self.g = g
		self.h = h
