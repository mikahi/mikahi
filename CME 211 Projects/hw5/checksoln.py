import sys
import numpy as np

if len(sys.argv) < 3:
	print('Usage:')
	print('  python {} [maze file] [solution file]'.format(sys.argv[0]))
	exit()

#initializes array 
header = np.loadtxt(sys.argv[1], dtype=int, delimiter=' ') 
row = header[0][0]
column = header[0][1]
walls = np.zeros((row, column))

data = np.loadtxt(sys.argv[1], dtype=int, delimiter=' ',  skiprows=1) 
for i in data:
	a =i[0]
	b =i[1]
	walls[a][b] =1

# Create an array from the solution text of all the x,y coordinates of the solution
data2 = np.loadtxt(sys.argv[2], dtype=int, delimiter=' ') 

# Check if the first step is in the first row of the maze.
if data2[0][0] != 0:
	print("You didn't enter from the first row of the maze.")
	exit()

# Check if the last step is in the last row of the maze.
if data2[-1][0] != row - 1:
	print("You didn't reach the terminal of the maze.")
	exit()

# Check if there is a wall in the solution.
for step in data2:
	y = step[1]
	x = step[0]
	if walls[x][y] == 1:
		print("You crossed the wall of the maze.")
		exit()

# see if all steps are consecutive 

iterations = range(len(data2)-1)

for i in iterations:
	x1 = data2[i][0]
	x2 = data2[i + 1][0]
	y1 = data2[i][1]
	y2 = data2[i + 1][1]
	deltax = abs(x1-x2) == 1
	deltay = abs (y1-y2) == 1
	valid1 = deltax ==1 and deltay ==0
	valid2 = deltax ==0 and deltay==1
	if (valid1 or valid2 == True):
		pass
	else:
		print("Some of your steps are not consecutive.")
		exit()

print("The solution is valid!")

