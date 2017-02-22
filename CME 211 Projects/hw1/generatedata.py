import random
import sys

#takes in the desired characteristics for the reads file and reference file
if __name__ == '__main__':
	if len(sys.argv) != 6:
		print('Usage:')
		print()
		exit()
	reference_length = int(sys.argv[1])
	nreads = int(sys.argv[2])
	read_length = int(sys.argv[3])
	reference_file = sys.argv[4]
	reads_file = sys.argv[5]

#function to generate a DNA string from numbers 
def randomletter (x):
	if x ==0 :
		return "A"
	if x ==1 :
		return "T"
	if x ==2:
		return "G"
	if x ==3:
		return "C"

#creates the first 75% of the reference string 
ref75 = ''
refindex =0
while refindex <reference_length *0.75:
	ref75+=randomletter(random.randint(0,3))
	refindex+=1

#creates the reference string by combining the whole 75% string and the last portion of the 75% string 
refstring = ref75 +ref75[int(reference_length*3/4-reference_length/4):]

#opens the reference file
reference = open(reference_file, 'w')

#writes the reference string into the reference file
reference.write(refstring)
reference.close()


reads = open(reads_file, 'w')

#initialize values to create reads file
readsStart=0
align0 = 0 #15%
align1 = 0 #75%
align2 =0 #10%

#creates the reads by going through the reads generation process for each number of reads 
while readsStart < nreads:
	randomrate = random.random()

#creates reads with one alignment 
	if randomrate <0.75: 
		stringStart = random.randint (1,reference_length/2)
		reads.write(refstring[stringStart : stringStart + read_length]+"\n")
		align1 +=1

#creates reads with two alignments 
	elif randomrate >= 0.75 and randomrate <0.85:
		stringStart = random.randint(reference_length*0.75, reference_length - read_length)
		reads.write(refstring[stringStart: stringStart + read_length]+"\n")
		align2+=1

#creates reads with no alignemnts 
	else:
		wrongreads = refstring[0]
		while refstring.find(wrongreads) != -1: 
			wrongreads=''
			nonalignindex=0
			while nonalignindex < read_length:
				wrongreads+=randomletter(random.randint(0,3))
				nonalignindex+=1
		reads.write(wrongreads+ "\n")
		align0+=1
#updates the number of lines generated 	
	readsStart+=1

reads.close()

#prints the info 
print('reference length: {}'.format(reference_length))
print('number reads: {}'.format(nreads))
print('read length: {}'.format(read_length))
print('aligns 0: {}'.format(float(align0)/float(nreads)))
print('aligns 1: {}'.format(float(align1)/float(nreads)))
print('aligns 2: {}'.format(float(align2)/float(nreads)))



