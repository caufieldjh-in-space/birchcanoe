#!/usr/bin/python
#birchcanoe.py
'''
Generates novels and their accompanying audio based on 
phonetically-optimal English sentences. #NaNoGenMo2017

Uses the Harvard Sentences - see
http://ieeexplore.ieee.org/document/1162058/
'''

import random, sys

#Contants and Setup

#Methods
def get_hsents():
	'''Retrieve the input sentences'''
	hsents = []
	with open("harvsents.txt") as hsfile:
		for line in hsfile:
			if line[0] != "H":
				cleanline = ((line.split("."))[1]).strip()
				hsents.append(cleanline)
	return hsents
	
def assemble_story(sents):
	'''Assemble the story.'''
	story = ""
	word_count = 0
	need_content = True
	
	ends = [".", "!"]
	
	while need_content:
		one_sent = random.choice(sents)
		end = random.choice(ends)
		story = ("%s%s%s ") % (story, one_sent, end) 
		word_count = word_count + len(one_sent.split())
		if word_count > 50000:
			need_content = False
	return story

#Main
def main():
	sents = get_hsents()
	story = assemble_story(sents)
	print(story)

if __name__ == "__main__":
	sys.exit(main())
