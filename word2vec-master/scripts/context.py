#!/usr/bin/
import subprocess
import time
import re
import os
import nltk
import string
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()

def runScript(word):
	#Run demo-script from word2vec tool with a word from the hashtag. Code in that script is modified to accept a parameter
	cmd= './runWordToVec.sh ' +  word + ''
	subprocess.call(cmd,shell=True)
	time.sleep(3)


def generateContext(filename) :

	#Generate Context list and append to a file for all the words in the hashtag that has length > 3
	words= []
	file = filename.split('.')[0]
	words.extend(file.split('_'))
	for word in words:
		if(len(word) > 3):
			runScript(wnl.lemmatize(word.lower()))


def getContextFromFileandDelete(filePath):

	#Creates a list of all the context from the output file and deletes the file
	context=[]

	with open(filePath) as f:
		
		for line in open(filePath):
			values = line
			for value in values.split('_'):
				lValue = wnl.lemmatize(value)
				context.extend(wnl.lemmatize(lValue))
	os.remove(filePath)
	return context
	

def loadHashTag(filePath):
	#Create list of all the tweets from the given filePath

	lines = []

	with open(filePath) as f:

		# Only the second column from the file is considered. Label and tweetID are ignored
		tweet = [line.split('\t')[1] for line in open(filePath)]

		#tweet = cleanData(tweet,Ofilename)

		lines.extend(tweet)

	return lines


def generateFeatureSet(context, tweetsList, filename):

	#Main method for creating the feature set.Counts the number of words within the context in a given tweet and creates a feature list
	
	i = 0;
	featureDict = {}
	for tweets in tweetsList:
		featureList = []
		count = 0
		key = filename.split('.')[0] + "_" + `i` + "_" + "Context"
		for iWord in nltk.word_tokenize(tweets):
			# Only consider words with length more than 3 to prevent most determiners and numbers (stop words)
			if(len(iWord) > 3):
				if(wnl.lemmatize(iWord.lower()) in context):
					count = count + 1
					#print iWord.lower()
		featureList.append(count)
		featureDict[key] = featureList
		i = i+1;

	print featureDict;

	return featureDict;


def cleanData(tweet,filename):


  	#Any necessary data cleaning should be performed here. Removes midnight, hashtags and any punctuations
  	cleanedList = []
  	r = re.compile(r"([#@])(\w+)\b")
  	wordtoReplace = filename.replace("_","").split(".")[0]

  	for lines in tweet:
  		
  		lines  = r.sub('',lines)	
  		lines= lines.translate(None, string.punctuation)  		
  		cleanedList.append(lines)

  	return cleanedList

  	

def runContextFeature(tweetsList,filename):

	#First Method to be called for running this script with tweets list and filename as parameters.

	
	generateContext(filename)
	context = getContextFromFileandDelete("context.out")
	featuredDict = generateFeatureSet(context,cleanData(tweetsList,filename),filename)

   	return featuredDict 



if __name__ == "__main__":

	directory = '/home/dhunganaa/Documents/data/trial_dir/trial_data'
	for filename in sorted(os.listdir(directory)):
		line = []
		featuredList = []
		
		#filename = 'Fast_Food_Books.tsv'
		filePath = directory + '/' + filename
		line.extend(loadHashTag(filePath))
		runContextFeature(line,filename)
	
	

	# for tweet in lines:
	# 	generateContext()

		

	



