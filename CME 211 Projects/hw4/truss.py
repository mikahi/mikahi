import numpy as np
import os
import warnings
import scipy.sparse.linalg as spla
import math
import glob
import matplotlib as mpl
import scipy.sparse as sparse
import os.path
mpl.use('Agg') 
import matplotlib.pyplot as plt


class Truss:

	def __init__(self, jointfile, beamfile):

		"""
		initialize all variables from beamfile and jointfile
		"""
		jointinfo = open(jointfile, 'r')
		beaminfo = open(beamfile, 'r')
		'''
		establish dicitonaries and the beam number 
		'''
		self.joints = {}
		self.beams = {}
		self.beamnum=0

		def numberCount(sequence, start=0):
			n = start
			for elem in sequence:
				yield n, elem
				n += 1

		for i, line in numberCount(jointinfo):
			if i == 0:
				pass
			else:
				joint, x, y, Fx, Fy, zerodisp = line.split()
				joint = int(joint)
		'''
		make another dictionary for each joint
		'''
				self.joints[joint] = {}
				self.joints[joint]['beams'] = {}
				self.joints[joint]['position'] = (float(x), float(y))
				self.joints[joint]['externalforce'] = (float(Fx), float(Fy))
				self.joints[joint]['zerodisp'] = int(zerodisp)

		for i, line in numberCount(beaminfo):
			if i == 0:
				pass
			else:
				beam, ja, jb = line.split()
				beam = int(beam)
				ja = int(ja)
				jb = int(jb)
				self.beams[beam] = (ja, jb)

		'''
		Compute the drection of force given by beams, in the form of (cos, sin)
		'''
				x1 = self.joints[jb]['position'][0]
				x2 = self.joints[ja]['position'][0]
				y1 = self.joints[jb]['position'][1]
				y2 = self.joints[ja]['position'][1]
				deltax = x1 - x2
				deltay = y1 - y2
				denom = math.sqrt(deltax ** 2 + deltay ** 2)
				self.joints[ja]['beams'][beam] = (-deltax/denom, -deltay/denom)
				self.joints[jb]['beams'][beam] = (deltax/denom, deltay/denom)

		jointinfo.close()
		beaminfo.close()

		self.beamnum = i

	def EstablishMatrix(self):
		"""
		Create the linear system Ax = b
		the matrix A is a sparse matrix initialized by csr_matrix.
		A is organized by columns [beam tension forces and reaction forces of the joint] and 
		rows [the values of joint x coordinates and joint y coordinates, e.g. joint1 x coo, joint 1 y coo, joint 2 x coo..etc]
		B is a matrix of the External forces (Fx and Fy).
		"""
		'''
		loop through the beams, given the joint its associated with, calculate the direction of force given the associated x and y value
		'''
		rigidtrack = 0
		trackrow = 0
		row_idx = []
		col_idx = []
		val_data = []
		matrix_B = []

		'''
		Use csr_matrix((val_data, col_idx, row_idx)) to initialize the sparse matrix.
		'''
		row_idx.append(0)

		for beam in self.beams.keys():
		'''
		append direction of force ja values and add to the column and row indexes
		'''
			for jo in self.beams[beam]:
				val_data.append(self.joints[jo]['beams'][beam][0])
				col_idx.append(beam)
				row_idx.append(2*(jo-1))
				trackrow+=1
		'''
		append values of the extrenal forces to matrix b
		'''
			matrix_B.append(- self.joints[jo]['externalforce'][0])
		'''
		append direction of force jb values and add to the column and row indexes
		'''
			for jo in self.beams[beam]:
				val_data.append(self.joints[jo]['beams'][beam][1])
				col_idx.append(beam)
				row_idx.append(2*(jo)+1)
				trackrow+=1
		'''
		append values of the extrenal forces to matrix b
		''' 	
			matrix_B.append(- self.joints[jo]['externalforce'][1])
		'''
		append the reaction forces of the joint to the matrix
		'''
		for jo in self.joints.keys():
			if self.joints[jo]['zerodisp']:
				val_data.append(1)
				col_idx.append(self.beamnum + 2 * rigidtrack + 1)
				rigidtrack += 1
				row_idx.append(2*(jo-1))
		

		'''
		Check if the number of rows and number of columns are equal, if not, raise an error.
		'''
		if len(matrix_B) != max(col_idx) + 1:
			raise RuntimeError ("Truss geometry not suitable for static equilbrium analysis.") from error
		'''
		create matrix through csr_matrix with the val_data, col_idx, and row_idx values 
		'''
		A = sparse.csr_matrix((np.array(val_data), np.array(col_idx), np.array(row_idx)))
		return A, np.array(matrix_B)

		warnings.filterwarnings('error')
		warnings.filterwarnings('ignore',category=np.VisibleDeprecationWarning)
		warnings.filterwarnings('ignore',category=DeprecationWarning)

		try:
			solution = spla.spsolve(A, matrix_B)
		except Exception as e:
			if 'Singular' in str(e):
				raise RuntimeError("Cannot solve the linear system, unstable truss?") from error

	def PlotGeometry(self, plotfile = None):
		'''
		plot geometry 
		'''
		plt.figure()
		for i in range(len(self.beams[:, 0])):
		'''store the two ends of a beam'''
			joint1 = self.beams[i, 1]
			joint2 = self.beams[i, 2]
		'''draw a line between the two joints to represent the beam'''
			plt.plot([self.joints[joint]['position'][0], \
				self.self.joints[joint]['position'][0]], \
				[self.joints[joint]['position'][joint1][1], \
				self.joints[joint]['position'][joint2][1]], \
				color = 'b')

		'''make plot nicer'''
		plt.axis('equal')
		'''save the plot'''
		plt.savefig(output)

	def __repr__(self):
		'''solve for the values of x from Ax = B through solving the sparse matrix'''
		A, matrix_B = self.EstablishMatrix()
		for beam in self.beams:
			self.beams[beam]['tension'] = spla.spsolve(A, matrix_B)[beam - 1]

		answer = list()
		answer.append("{0}{1: >9}".format("Beam".center(8), "Force"))
		answer.append('--------------------')
		for be in self.beams:
			finalval = (len('{}'.format(be))) * ' ' + '{}'.format(be) + \
			(12-len('{0:.3f}'.format(self.beams[be]['tension']))) \
			* ' ' + '{0:.3f}'.format(self.beams[be]['tension'])
			answer.append(finalval)
		return '\n'.join(answer)
