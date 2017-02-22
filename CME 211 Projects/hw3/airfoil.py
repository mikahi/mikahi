import os.path
import sys
import glob
import os
import math
import operator

#creates Airfoil class 
class Airfoil:
	def __init__(self, inputdir):
		#creates variables to be used later 
		self.name = ''
		self.x = list()
		self.y = list()
		self.alphas = list()
		self.cp = {}
		self.cdeltas = {}

	#ensures you are in the right working directory
		dirdir, dirbase = os.path.split(os.path.abspath(inputdir))
		if dirdir != os.getcwd():
			os.chdir(dirdir)

		# Check if the directory exists. 
		if not os.path.exists(dirbase):
			raise RuntimeError("The directory doesn't exist!")

		# Check if the required files exist. 
		if len(glob.glob(dirbase + '/xy.dat')) == 0:
			raise RuntimeError("The file w/ xy coordinates does not exist!")
		if len(glob.glob(dirbase + '/alpha*.dat')) == 0:
			raise RuntimeError("The alpha values file does not exist!")

		self.name = self.loadfile(inputdir) 

#loads entire file from the input 
	def loadfile(self, inputdir): 
		dirfile = glob.glob(inputdir)
		for i in range (len(dirfile)):
			#loads xy variables
			xyfile = os.path.join(inputdir,'xy.dat')
			xyfile = open(xyfile, 'r')
			coordinates = xyfile.readline().strip()
			for line in xyfile:	
				self.x.append(float((line.split()[0])))
				self.y.append(float(line.split()[1]))
			#loads alpha variabls
			alphafile = glob.glob(os.path.join(inputdir,'alpha*.dat'))
			for alphaval in alphafile:
				alphaValue = os.path.split(alphaval)[-1][5:-4] 
				self.alphas.append(float(alphaValue))
				alpha = list()
				f = open(alphaval)
				f.readline()
				for line in f:
					alpha.append(float(line.strip()))
				f.close()
				self.cp[float(alphaValue)] = alpha # makes a dict {cp (pressure coeff) : corresponding alphas}

		return coordinates


	#finds the length of the chord by inputting the max and min of x and finding the absolute value of max-min
	def chord_length(self):

		minimum_x = min(abs(x) for x in self.x)
		maximum_x = max(abs(x) for x in self.x)
		length = abs(maximum_x - minimum_x)

		return length

#finds the lift coefficient by computing for deltax & delta7, and the deltaCx and deltaCy
#these values are then used to compute for cl with the formula given in the assignemnt 
	def lift_coeff(self, alpha):


			cx = 0
			cy = 0
			self.cdeltas[alpha] = list()
			for index in range(len(self.cp[alpha])):
				deltax = self.x[index]- self.x[index+1]
				deltay = self.y[index]- self.y[index+1]
				cdeltax =  - self.cp[alpha][index] * deltay / self.chord_length()
				cdeltay = self.cp[alpha][index] * deltax / self.chord_length()
				self.cdeltas[alpha].append((cdeltax, cdeltay))
				cx += self.cdeltas[alpha][index][0]
				cy += self.cdeltas[alpha][index][1]
			cl = -1*cy * math.cos(alpha * math.pi/180) - cx * math.sin(alpha * math.pi/180)
			return cl

#finds stagnation point by fiinding the error in the alphas (whatever is closest to 0)
#index err is used to keep track of which ith value this error is found at so the x and y averages can be recorded
#the stagnation point is returned as a dictionary with the x and y average and the corresponding cp
	def stagnation_point(self):
		ret = {}
		for alpha in self.alphas:
			err_1 = float('+inf')
			index_i=0
			for i in range(len(self.cp[alpha])):
				# print(self.cp[alpha])
				err =  abs(1.0 - self.cp[alpha][i])
				if err < err_1:
					err_1 = err
					index_err = i 
			y_avg = (self.y[index_err] + self.y[index_err+1])/2.0
			x_avg = (self.x[index_err] + self.x[index_err+1])/2.0
			ret[alpha] = (x_avg, y_avg, self.cp[alpha][index_err])
		return ret

#prints out the values 
	def __repr__(self):
		string = "Test case: {}\n".format(self.name)
		string += "\nalpha    cl          stagnation pt      \n"
		string += "----- ------- --------------------------\n"
#table is sorted by increasing order of alpha 
		alphas = sorted(self.alphas)
		res_dict = self.stagnation_point()
		for i in range(len(alphas)):
			cl = self.lift_coeff(alphas[i]) 
			stag_x, stag_y, val = res_dict[alphas[i]]
			string += "{0:>5.2f} {1:>7.4f} ( {2:<6.4f}, {3:>7.4f}) {4:>7.4f}\n". \
				format(alphas[i], cl, stag_x, stag_y, val)
			
		return string 

