import sys
import math
import time
import operator
import random
from collections import defaultdict
import numpy as np
from scipy import spatial


#function to get specific item in a list of items
def getitem(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g

#adjusted cosine similarity function 
def cosineSim(x, y):
	average_x = np.mean(x)
	average_y = np.mean(y)
	summation_x = 0
	summation_y = 0
	summation_xy = 0
	for i in range(len(x)):
		difference_x = x[i] - average_x
		difference_y = y[i] - average_y
		summation_xy += difference_x * difference_y
		summation_x += difference_x ** 2
		summation_y += difference_y ** 2
	cossim = summation_xy / math.sqrt(summation_x * summation_y)
	return cossim

#gives list of common users for one movie. This iterates through two dictionaries and retrivees the list of users, and turns 
#them into sets, combines these sets into a list
def commonUsers (dict1, dict2):
	a = set(dict1.keys())
	b = set(dict2.keys())
	same_user = list(a & b)
	return same_user

#gets input from user 
if len(sys.argv) < 3:
	print('Usage:\npython similarity.py <MovieLens file> <similarities file> [user thresh (default = 7)] [maximunm results (default = 3)]')
	exit()
movie_data = sys.argv[1]
finalresult = sys.argv[2]
if len(sys.argv) < 4:
	threshold = 5
elif len(sys.argv) < 5:
	threshold = int(sys.argv[3])
else:
	threshold = int(sys.argv[3])

document = open(movie_data, 'r')

line_index=0

user_set = set()
movie_set = set()
ratings = {}

#makes dictionary for movieID, user, and score. This is a dictionary within a dictionary. The key of the first dictionary is the userID
# the value of the first dictionary is the movieID. the key of the second dictionary is the whole first dictionary, and the value is the 
#rating of the movie. This also creates lists for userIDs, moveIds, and the rating so that the length of movies and users can be printed out.

answer = {}
for line in document.readlines():
    line = line.strip()
    line = line.split()
    line_index += 1
    if not line: 
        continue
    if int(line[1]) not in answer:
      	answer[int(line[1])] = {}
    answer[int(line[1])][int(line[0])] = int(line[2])
    userid = int(line[0])
    movieid = int(line[1])
    rating = int(line[2])
    user_set.add(userid)
    movie_set.add(movieid)
    ratings[(userid, movieid)] = rating

users = list(user_set)
movies = list(movie_set)

#prints outputs

print("Input MovieLens file: {}".format(sys.argv[1]))
print("Output file for similarity data: {}".format(sys.argv[2]))
print("Minimum number of common users: {}".format(threshold))
print("Read {} lines with total of {} movies and {} users".format(line_index, len(movies), len(users)))

st = time.time()

# This stores a dictionary of the similarity of two movies and the number of people who rated these two movies as such :(first movie, second movie): (similarity, # of people who rated both movies)
#double for loop is used to iterate through all the movies in the answer.keys() dictionary. 
#cosineSim is used to find pearson coefficient for between two ratings (which have been iterated over)

movie_group = {}

for movie_1 in answer.keys():
	for movie_2 in answer.keys():
		if movie_1 == movie_2: continue
		match1 = commonUsers(answer[movie_1], answer[movie_2])
		if len(match1) >= threshold:
			rating_1 = [answer[movie_1][u] for u in match1]
			rating_2 = [answer[movie_2][u] for u in match1]
			movie_group[(movie_1, movie_2)] = (cosineSim(rating_1, rating_2), len(match1))
		else:
			movie_group[(movie_1 ,movie_2)] = 0


#makes a dictionary for recommendations in the following order: {said movie: [(recommended movie, similarity, # of useres)}
#double for loop is used to iterate through all possible matches.

recommendation = {}

for movieid in range(len(movies)):
	recommendation[movies[movieid]] = list()
for movie_1 in answer.keys():
	for movie_2 in answer.keys():
		if movie_group[(movies[movie_1], movies[movie_2])]  != 0:
			recommendation[movies[movie_1]].append((movies[movie_2], movie_group[(movies[movie_1], movies[movie_2])][0], movie_group[(movies[movie_1], movies[movie_2])][1]))
			recommendation[movies[movie_2]].append((movies[movie_1], movie_group[(movies[movie_1], movies[movie_2])][0], movie_group[(movies[movie_1], movies[movie_2])][1]))

# Sorts the recommendation results according to their similarity (highest sim followed by successively lower similarities)
#
for movieid in answer.keys():
	original = recommendation[movies[movieid]]
	new = sorted(original, reverse = True, key = getitem(1))
	recommendation[movies[movieid]] = new 

final_recommendations = open(finalresult, 'w')

# Recommendation results are printed for all movies 
# this writes the recommendations file by retrieving the movie number, 
#the simialriy coefficient, and the number of common users. it is all written into the recommendations file. 
for movieid in answer.keys():
	final_recommendations.write(str(movies[movieid]) + ' ')
	for numberRecs in range(len(recommendation[movies[movieid]])):
		if cossim > 0:
			final_recommendations.write('(' + str(recommendation[movie]) + ',' + str(round(recommendation[movies[movieid]]), 2) + ',' + str(recommendation[movies[movieid][numberRecs]]) + ') ')
	final_recommendations.write('\n')

endtime = time.time()

print("Computed simiarities in {} seconds".format(endtime - st))


document.close()
final_recommendations.close()
