import nltk  
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from nltk.corpus import treebank_chunk 
import json 
import itertools
import re
def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False
def extract_questions(file_name):
	'''Extracts question from a json file in the given format
		param:
			file_name: Json file
		return:
			list_of_questions:List'''
	list_of_questions=[]
	with open(file_name,'rb') as file:
		file_data=json.load(file)
	for question_dict in file_data:
		list_of_questions.append(question_dict['Question'])
	return list_of_questions
def load_stop_words(stop_word_file):
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words
def build_stop_word_regex(stop_word_file_path='stop_word_list.txt'):
    stop_word_list = load_stop_words(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern
def extract_candidate_keywords(question,stopword_pattern):
	phrase_list = []
	
	tmp = re.sub(stopword_pattern, '|', question.strip())
	phrases = tmp.split("|")
	for phrase in phrases:
		phrase = phrase.strip().lower()
		if phrase != "":
			phrase_list.append(phrase)
	return phrase_list
	
def separate_words(text, min_word_return_size):
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words

def calculate_word_scores(phraseList):
	word_frequency = {}
	word_degree = {}
	for phrase in phraseList:
		word_list = separate_words(phrase, 0)
		word_list_length = len(word_list)
		word_list_degree = word_list_length - 1
		for word in word_list:
			word_frequency.setdefault(word, 0)
			word_frequency[word] += 1
			word_degree.setdefault(word, 0)
			word_degree[word] += word_list_degree  
	for item in word_frequency:
		word_degree[item] = word_degree[item] + word_frequency[item]		

	word_score = {}
	for item in word_frequency:
		word_score.setdefault(item, 0)
		word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  
    
	return word_score
def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates
def main():
	questions=extract_questions('result.json')
	keywords_list[]
	for question in questions:
		question=question.lower()
		question=re.match(r'[^.!?,;:\t\\\\"\\(\\)\\\'\u2013\-\_]+',question).group()
		stop_word_pattern=build_stop_word_regex()
		phrase_list=extract_candidate_keywords(question,stop_word_pattern)
		word_scores = calculate_word_scores(phrase_list)

		keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)
		sorted_keywords = sorted(keyword_candidates.items(), reverse=True)
		keywords_list.append(sorted_keywords)
	return keywords_list
		
		
main()