import sys
import math
import matplotlib.pyplot as plt
import numpy as np


def solve(inpt, soln_file):
	# check usage message input
	# read in the basic geometry information of the pipe
	f = open(inpt, 'r')
	for i, line in enumerate(f):
		if i ==0:
			L,W,h = line.split()
			L = float(L)
			W = float(W)
			h = float(h)
		else:
			Tc, Th = line.split()
			Tc = float(Tc)
			Th = float(Th)
	f.close()

	soln = np.loadtxt(soln_file)

	# dimension of the pipe
	ncol = int((L/h) + 1) #m
	nrow = int((W/h) + 1) #n

	solution = np.zeros((nrow, ncol), dtype = np.float64)

	# build the pipe
	# add boundary points into the pipe
	# hot isothermal boundary
	solution[0] = Th
	solution[1 : nrow - 1, 0 : ncol - 1] = soln.reshape(nrow - 2, ncol - 1)
	solution[1 : nrow - 1, ncol - 1] = solution[1 : nrow - 1, 0]
	# cold isothermal bou ndary
	solution[nrow - 1] = (-1) * Tc * (np.exp(-10 * np.power(np.array(range(ncol)) * h - L/2, 2)) - 2)

	#find mean temp
	mean_temp = np.mean(solution)
    
	print("Mean Temperature: {}".format(np.around(mean_temp, decimals = 5)))


	# Now let us plot the thermal plot
	plt.figure()
	plt.axis('equal')
	x = np.arange(0, L + h, h)
	y = np.arange(0, W + h, h)
	X, Y = np.meshgrid(x, y)

	plt.pcolormesh(X, Y, solution)
	plt.colorbar()

	# Set up the axis in a proper scale.
	plt.axis([x.min(), x.max(), -y.max(), 2 * y.max()])
	plt.xlabel('X')
	plt.ylabel('Y')

	#  plot the isoline
	plt.contour(X, Y, pipe, [mean_temp], color = 'black', linestyle = '-')
	plt.savefig('figure.jpg')
	plt.show()
	
#run the postprocess code
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:\n $ python checksoln.py [inputx.txt] [solution<#>.txt] ") 
        sys.exit()
    if len(sys.argv)==3:        
        a=solve(sys.argv[1],sys.argv[2])
        print('Input file processed:{}'.format(sys.argv[1]))
