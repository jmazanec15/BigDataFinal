#!/usr/bin/env python2.7
import pandas as pd
import ast # converts string to dict
from afinn import Afinn # Sentiment score
import sys

'''
How we're going to rate recommendations:
1. Likes and dislikes on similar talks ~ everyone starts out with 0	
2. get sentiment score on each rating and multiply it by the number of ratings
Keep track of speeches that have already been recommended
'''

def init():
	## Read in data about tags
	ted_main = pd.read_csv('data/ted_main.csv')
	pq = list()
	afinn = Afinn()
	## Get all tags and their views and freq
	# Loop through each talk and get/set tags data
	for i in range(len(ted_main)):
		ratings =  ast.literal_eval(ted_main['ratings'][i])
		title = ted_main['title'][i]
		score = 0
		for rating in ratings:
			score += afinn.score(rating['name']) * rating['count']
		pq.append([0, score, title, 0])
		pq.sort(reverse=True)
	return pq

def main():
	## Init the priority queue, it'll come sorted
	pq_talks = init()
	## Continue to loop until everything is gone
	while True:
		while True:
			print "Enter 0 for the next rec\nEnter 1 to rate a Ted talk"
			inp = input()
			if inp == 0 or inp == 1:
				break
		# React to users choice
		if inp == 0:
			index = 0
			for i in range(len(pq_talks)):
				if pq_talks[i][3] == 0:
					index = i
					break
			print "We recommend you listen to '" + pq_talks[index][2] + "'"
			pq_talks[index][3] = 1
			while True:
				print "Do you want to listen to this? Enter 1 for yes, Enter -1 for no"
				rating = input()
				if rating == -1 or rating == 1:
					break
			# Now find the title in the data and flag all the related talks

		else:
			pass
		pq_talks.sort(reverse=True)


if __name__ == "__main__":
	main()