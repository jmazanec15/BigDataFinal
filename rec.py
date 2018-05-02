#!/usr/bin/env python2.7
import pandas as pd
import ast # converts string to dict
from afinn import Afinn # Sentiment score

'''
How we're going to rate recommendations:
1. Likes and dislikes on similar talks ~ everyone starts out with 0	
2. get sentiment score on each rating and multiply it by the number of ratings
Keep track of speeches that have already been recommended and change ratings 
based on ratings of similar talks
'''

## Initialize dictionary for all talks
# Reads in all talks and scores their ratings
def init():
	## Read in data about tags
	ted_main = pd.read_csv('data/ted_main.csv')
	pq = dict()
	afinn = Afinn()
	## Get all tags and their views and freq
	# Loop through each talk and get/set tags data
	for i in range(len(ted_main)):
		ratings =  ast.literal_eval(ted_main['ratings'][i])
		title = ted_main['title'][i]
		score = 0
		for rating in ratings:
			score += afinn.score(rating['name']) * rating['count']
		pq[title] = [0, score, 0]
	return pq

## Converts the dictionary of talks into a sorted list of just the titles
def get_list(pq_dict):
	pq = list()
	for key in pq_dict:
		pq.append([pq_dict[key][0], pq_dict[key][1], key])
	pq.sort(reverse=True)
	return [p[2] for p in pq]

## Set up dictionary of related talks
def set_related_talks():
	## Read in data about tags
	ted_main = pd.read_csv('data/ted_main.csv')
	related_talks = dict()
	## Get all tags and their views and freq
	# Loop through each talk and get/set tags data
	for i in range(len(ted_main)):  
		titles = [talk['title'] for talk in ast.literal_eval(ted_main['related_talks'][i])]
		related_talks[ted_main['title'][i]] = titles
	return related_talks



def main():
	## Init the priority queue, it'll come sorted
	pq_talks = init()
	related_talks = set_related_talks()
	pq_list = get_list(pq_talks)
	## Read input
	# Continue to loop until everything is gone
	while True:
		while True:
			print "Enter 0 for the next rec\nEnter 1 to rate a Ted talk"
			inp = input()
			if inp == 0 or inp == 1:
				break
		# React to users choice
		if inp == 0:
			# Find first recommendation that hasnt already been rec'd
			index = 0
			for i in range(len(pq_talks)):
				if pq_talks[pq_list[i]][2] == 0:
					print "here"
					index = i
					break
			print "We recommend you listen to '" + pq_list[index] + "'"
			# Mark title as recommended
			pq_talks[pq_list[index]][2] = 1
			# Get user feedback
			while True:
				print "Do you want to listen to this? Enter 1 for yes, Enter -1 for no"
				rating = input()
				if rating == -1 or rating == 1:
					break
			# Update that talks rating
			pq_talks[pq_list[index]][0] += rating
			# Now update rating for all of its related talks
			for talk in related_talks[pq_list[index]]:
				pq_talks[talk][0] += rating
		else:
			# Get rating for a speech the user already listened to
			print "Enter the title of the talk:"
			talk = raw_input().rstrip()
			# Validity check
			while talk not in pq_talks:
				print "Talk not found"
				talk = raw_input().rstrip()
			print "Did you like it? Enter 1 for yes, Enter -1 for no"
			rating = input()
			while rating != -1 and rating != 1:
				print "Error try again"
				rating = input()
			# Update rating and mark as listened to
			pq_talks[talk][2] = 1
			pq_talks[talk][0] += rating
			# Now flag all of its related talks here
			for t in related_talks[talk]:
				pq_talks[t][0] += rating	
		# Reset list with updated information
		pq_list = get_list(pq_talks)

if __name__ == "__main__":
	main()