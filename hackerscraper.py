#!/usr/bin/python3

import sys, os, requests, json, re, random

# TODO: try catches

'''
HackerScraper: "one that opens the leading article on hacker news at that moment and prints x number of comments to the command line"

Credit to Sean for the... prompt.

Usage:
hackerscraper.py [numcomments]

Argument(s):

	numcomments: number of top comments to load.

'''



if __name__ == '__main__':
	if len(sys.argv) < 2:
		numcomments = 3
	else:
		try:
			numcomments = int(sys.argv[1])
		except:
			numcomments = 3

	url = "https://hacker-news.firebaseio.com/v0/"

	request = requests.get(url + "topstories.json")
	topstories = request.json()

	# topstories[0] is the top news story
	# now request that story

	request = requests.get(url + "item/" + str(topstories[0]) + ".json")
	topstory = request.json()

	print(topstory['title'] + "\n")

	# truncate numcomments if the story has less than numcomments comments
	numcomments = numcomments if len(topstory['kids']) > numcomments else len(topstory['kids'])
	for i in range(0,numcomments):
		request = requests.get(url + "item/" + str((topstory['kids'])[i]) + ".json")
		comment = request.json()
		print(comment['text'] + "\n")