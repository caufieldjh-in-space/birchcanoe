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

import random, sys
import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
import sklearn.feature_extraction.text

#Contants and Setup
max_word_count = 50000

#nltk.download('punkt')
#sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#Classes
class ExtendPunktTokenizer(PunktLanguageVars):
	sent_end_chars = ('.', '?', '!', '\n')

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
	
	word_count = 0
	need_content = True
	
	#ends = [".", "!"]
	ends = ["."]
	chapbreak = ("***")
	
	chap_word_count = 0
	chap_count = 1
	this_chap_len = random.randint(3000,5000)
	
	story = ("***")
	
	one_sent = random.choice(sents) + random.choice(ends)
	story = ("%s%s ") % (story, one_sent)
	
	while need_content:
		new_words = []
		sample = one_sent.split()
		for _ in xrange(1,3):
			new_words.append((random.choice(sample)).lower())
		story = ("%s%s ") % (story, " ".join(new_words))
		
		word_count = word_count + len(new_words)
		chap_word_count = chap_word_count + len(new_words)
		
		if chap_word_count > this_chap_len:
			
			story = ("%s%s") % (story, chapbreak)
			
			one_sent = random.choice(sents) + random.choice(ends)
			word_count = word_count + len(one_sent.split())
			story = ("%s%s ") % (story, one_sent)
			
			chap_count = chap_count +1
			chap_word_count = 0
			this_chap_len = random.randint(3000,5000)
			
			new_words = []
			
		if word_count > max_word_count:
			need_content = False
			
	return story
	
def clean_story(story):
	'''Do final formatting adjustments.'''
	sent_tokenizer = PunktSentenceTokenizer(lang_vars = ExtendPunktTokenizer())
	all_chaps = story.split("***")
	tok_story = []
	
	chap_num = 1
	
	for chap in all_chaps:
		tok_chap = sent_tokenizer.tokenize(chap)
		cleanchap = " ".join([sentence.capitalize() for sentence in tok_chap])
		tok_story.append("--- %s ---" % chap_num)
		chap_num = chap_num +1
		tok_story.append(cleanchap)
	
	cleanstory = "\n\n".join(tok_story)
	
	return cleanstory

#Main
def main():
	sents = get_hsents()
	story = assemble_story(sents)
	story = clean_story(story)
	print(story)

if __name__ == "__main__":
	sys.exit(main())
