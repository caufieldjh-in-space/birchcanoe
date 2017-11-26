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

from numpy.random import choice

import wikipedia

import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
import sklearn.feature_extraction.text

#Contants and Setup
max_word_count = 50000

for item in ['punkt', 'averaged_perceptron_tagger']:
	nltk.download(item)
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
	
def get_new_material():
	'''Retrieve new vocabulary from randomly-chosen external sources.
		Mostly Wikipedia.
		Returns dictionary with POS types as keys and lists of
		corresponding strings as values.'''
	
	all_content = []
	all_tagged_content = []
	new_material = {}
	
	need_items = True
	
	while need_items:
		try:
			random_wp_items = wikipedia.random(pages=3)
			for item in random_wp_items:
				this_page = wikipedia.page(item)
				content = this_page.content
				all_content.append(content)
			need_items = False
		except wikipedia.exceptions.DisambiguationError:
			pass
	
	for content in all_content:
		tok_content = nltk.word_tokenize(content)
		one_tag_set = nltk.pos_tag(tok_content)
		all_tagged_content.append(one_tag_set)
	
	all_tags_together = [item for sublist in all_tagged_content for item in sublist]
	for item in all_tags_together:
		tag = item[1]
		token = item[0]
		if token in [u"==", u"===", u"/"]:
			continue
		if tag not in new_material:
			new_material[tag] = [token]
		else:
			new_material[tag].append(token)
	
	return new_material 
	
def write_chapter(sents, new_material):
	'''Write a single chapter (a continuous string, with newlines).'''
	
	this_chap_len = random.randint(3000,5000)
	
	one_end = (choice(ends, 1, p=[0.95, 0.05]))[0]
	one_sent = ("%s%s ") % (random.choice(sents), one_end)
	sample = one_sent.split()
	chap_word_count = len(sample)
	
	#Get the parts of speech in this seed sentence.
	tok_content = nltk.word_tokenize(one_sent)
	raw_form = nltk.pos_tag(tok_content)
	
	need_content = True
	chap = one_sent
	
	while need_content:
		new_words = []
		for item in raw_form[:-1]: #Do replacement here. Skip final punct.
			token = item[0]
			tag = item[1]
			if choice([0,1], 1, p=[0.75, 0.25])[0] == 1:
				new_token = u"..."
				try:
					new_token = random.choice(new_material[tag])
				except KeyError: 
					#Thrown if we don't have options for this POS
					new_words.append(token)
				new_words.append(new_token)
			else:
				new_words.append(token)
		new_sent = " ".join(new_words)
		one_end = (choice(ends, 1, p=[0.9, 0.1]))[0]
		new_sent = new_sent[0].upper() + new_sent[1:].lower().rstrip() + one_end
		chap = ("%s%s ") % (chap, new_sent)
		chap_word_count = chap_word_count + len(new_words)
		if random.randint(0,4) == 0:
			chap = chap + "\n\n"
		if chap_word_count > this_chap_len:
			need_content = False
	
	return (chap, chap_word_count)
	
def assemble_story(sents, new_material):
	'''Assemble the story.
		Ideally, the title of each chapter should reflect content.'''
	
	word_count = 0
	chap_count = 1
	
	need_chaps = True
	story = ""

	while need_chaps:
		new_chap, new_chap_len = write_chapter(sents, new_material)
		story = ("%s\n\n---%s---\n%s") % (story, str(chap_count), new_chap)
		
		word_count = word_count + new_chap_len
		
		chap_count = chap_count + 1
		
		if word_count > max_word_count:
			need_chaps = False
			
	return story
	
#Main
def main():
	sents = get_hsents()
	new_material = get_new_material()
	story = assemble_story(sents, new_material)
	#print(story)
	
	story_file_name = str(random.randint(0,(10**10))) + ".txt"
	with open(story_file_name, 'w') as story_file:
		encoded = story.encode('ascii', 'ignore')
		story_file.write(encoded)
	print("Complete. See %s for output." % story_file_name)
	

if __name__ == "__main__":
	sys.exit(main())
