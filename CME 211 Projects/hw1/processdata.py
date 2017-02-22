import sys
import time

#takes in the desired files for processing 
if __name__ == '__main__':
	if len(sys.argv) != 4:
		print('Usage:')
		print()
		exit()
	REFFILE = sys.argv[1]
	READFILE = sys.argv[2]
	ALIGNFILE = sys.argv[3]

#opens the files 
reference_file = open(REFFILE,"r") 
reads_file = open(READFILE,"r")
align_file = open(ALIGNFILE, 'w')
readslength = 50

#counts the number of characters in the file 
chars = 0
words = 0
lines = 0
with open(REFFILE, 'r') as in_file:
    for line in in_file:
        lines += 1
        words += len(line.split())
        chars += len(line)

referenceString = reference_file.read()
referenceLength = chars 

reads_file = open(READFILE, 'r')

#starts the time for recording 
starttime = time.time()

readstart = 0
alignment0 =0
alignment1 = 0
alignment2 = 0
position=0
newposition=0
alignmentPosition=0
count=0

#goes through each line in the reads file and records how many times there is an alignment 

for i in reads_file.readlines():
	readsnow = i[:-1]
	position = referenceString.find(readsnow) 

#if there is an alignemnt  
	if position != -1:
		newposition = referenceString[position + readslength:].find(readsnow)
		#if there is one alignment 
		if newposition == -1:
			alignment1 +=1
			alignmentPosition = position
		#if there are two alignemnts 
		else:
			alignment2 +=1
			alignemntPosition = str(position) + str(newposition)
	#if there is no alignment 
	else:
		alignment0+=1
		alignmentPosition = -1

	#records the alignment position 
	align_file.write(readsnow+ ' ' + str(alignmentPosition))

	readstart+=1
	#increases the recorded number of iterations to record the number of reads  
	count+=1

reference_file.close()
reads_file.close()
align_file.close()

#records time
stoptime = time.time()
totaltime = stoptime-starttime

#prints info 
print('reference length: {}'.format(referenceLength))
print('number reads: {}'.format(count))
print('aligns 0: {}'.format(float(alignment0)/float(count)))
print('aligns 1: {}'.format(float(alignment1)/float(count)))
print('aligns 2: {}'.format(float(alignment2)/float(count)))
print('elapsed time: {}'.format(totaltime))





