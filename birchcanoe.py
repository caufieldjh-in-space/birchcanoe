#!/usr/bin/python
#birchcanoe.py
'''
Generates novels and their accompanying audio based on 
phonetically-optimal English sentences. #NaNoGenMo2017

Uses the Harvard Sentences - see
http://ieeexplore.ieee.org/document/1162058/

The overall goal is to use these sentences as seeds for each chapter.

Next steps:
* Build sentence classifier to identify how similar a given
  sentence is to a Harvard Sentence.
* Source sentences from Project Gutenberg texts and Wikimedia content.
* Build simple topical similarity model (non-structural features;
  start with topic lookup and hypo/hypernyms, also WordNet)
* Expand chapters with new material relevant to seed sentences.
* Arrange chapters more logically.
'''

import random, string, sys
import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
import sklearn.feature_extraction.text

#Contants and Setup
max_word_count = 50000

nltk.download('punkt')
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

ends = [".", "!"]

#Classes

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

def write_chapter(sents):
	'''Write a single chapter (a continuous string, with newlines).'''
	
	this_chap_len = random.randint(3000,5000)
	
	one_sent = ("%s%s ") % (random.choice(sents), random.choice(ends))
	sample = one_sent.split()
	chap_word_count = len(sample)
	
	need_content = True
	chap = one_sent
	
	while need_content:
		new_words = []
		for _ in xrange(1,5):
			new_words.append((random.choice(sample)).lower())
		new_sent = " ".join(new_words)
		new_sent = new_sent.translate(None, string.punctuation)
		new_sent = new_sent[0].upper() + new_sent[1:].lower() + random.choice(ends)
		chap = ("%s%s ") % (chap, new_sent)
		chap_word_count = chap_word_count + len(new_words)
		if random.randint(0,4) == 0:
			chap = chap + "\n\n"
		if chap_word_count > this_chap_len:
			need_content = False
	
	return (chap, chap_word_count)
	
def assemble_story(sents):
	'''Assemble the story.'''
	
	word_count = 0
	chap_count = 1
	
	need_chaps = True
	story = ""

	while need_chaps:
		new_chap, new_chap_len = write_chapter(sents)
		story = ("%s\n\n---%s---\n%s") % (story, str(chap_count), new_chap)
		
		word_count = word_count + new_chap_len
		
		chap_count = chap_count + 1
		
		if word_count > max_word_count:
			need_chaps = False
			
	return story
	
#Main
def main():
	sents = get_hsents()
	story = assemble_story(sents)
	print(story)
	
	story_file_name = str(random.randint(0,(10**10))) + ".txt"
	with open(story_file_name, 'w') as story_file:
		story_file.write(story)
	

if __name__ == "__main__":
	sys.exit(main())
