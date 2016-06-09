CSE 190 Final Project Write-up
Xavier Tejeda A10542023

Github Repository: https://github.com/xtejeda/CSE190_FinalProject.git
YouTube: 
Files:
	Robot.py	astar.py	CSE_190_Arduino.ino
Objective:
To emulate the A* implementation and simulation in PA3 on actual hardware. With each move that is published, a message is published to a topic which the Arduino can read from. Each LED represents a direction which will light up when the corresponding move is made.
Milestones:
1)	Get LED to blink.
2)	Get 4 LEDs to blink (one for each direction)
3)	Subscribe to ROS topic in order to determine which lights to blink.
a.	Rosserial_arduino library
http://wiki.ros.org/rosserial_arduino/Tutorials/Arduino%20IDE%20Setup 
 
Conclusions:
The largest issue I ran into was making sure that the LEDs had enough time to blink between moves. Serial communication also proved to be a challenge in regard to message types. I hope to further this project by replacing the LEDs with DC motors, and eventually moving onward to an RC car with a scaled map that falls in sync with the maps in PA3.
 
