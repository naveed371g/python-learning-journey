#!/usr/bin/env python3

def word_count(text):
	counts={}
	for word in text.split():
		if word in counts:
			counts[word] +=1
		else:
			counts[word]=1
	return counts

print(word_count("apple apple apple banana apple pears pears"))

