import sys
import truss

if len(sys.argv) < 3:
	print('Usage:')
	print('python {} [joints file] [beams file] [optional plot output file]'.format(sys.argv[0]))
	exit()

jointfile = sys.argv[1]
beamfile = sys.argv[2]
output_file = None

try:
	trussPrint = truss.Truss(jointfile, beamfile)
except Exception as e:
	print('ERROR: {}'.format(e))
	exit()

#  get static equilibrium truss object.
trussPrint.EstablishMatrix()

if len(sys.argv) >= 4:
	trussPrint.PlotGeometry(sys.argv[3])

print(trussPrint)
