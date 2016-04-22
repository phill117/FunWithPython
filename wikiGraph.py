#!/usr/bin/python3

import sys, os, requests, json, re, random

# TODO: try catches

'''
wikiGraph

Usage:
wikiGraph.py article

Argument(s):

	article: article name to load

'''

try:
	import networkx as nx
except:
	print("You need to install networkx. Use 'pip install networkx'.")

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# load wiki page

if __name__ == '__main__':
	if len(sys.argv) > 1:
		articleName = sys.argv[1]
		
	wikiURL = "https://en.wikipedia.org/w/api.php?action=query&rvprop=content&prop=revisions&rvsection=0&format=json&titles="
	
	request = requests.get(wikiURL + articleName)
	article = request.json()
	articleText = article['query']['pages'][list(article['query']['pages'].keys())[0]]['revisions'][0]['*']
	
	#someKindofRegex = '\\[\\[([()A-z0-9 .,\'"]+)[\|]?([()A-z0-9 .,"\']+)?\\]\\]'
	someKindofRegex = '\\[\\[(.*?)(?:\|(.*?))?\\]\\]'
	searches = re.findall(someKindofRegex,articleText)
	connections = set()
	#graph = graphviz.Digraph(comment='Connected Articles')
	#graph.node(articleName)
	graph = nx.DiGraph()
	
	for result in searches:
		connections.add(result[0])
		#graph.edge(articleName, result[0])
		graph.add_edge(articleName,result[0])
	print(connections)
	#graph.render(filename='wikiGraphs/'+articleName)
	plt.figure(num=None, figsize=(20, 20), dpi=120)
	node_labels = {node:node for node in graph.nodes()}
	nx.draw(graph, cmap=plt.get_cmap('jet'), node_color="0.8", node_size=4000, with_labels=True)
	#nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph), labels=node_labels)
	#plt.show()
	plt.savefig("wikiGraphs/" + articleName + ".png")
	
		