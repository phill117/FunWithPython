#!/usr/bin/python3

import sys, os, requests, requests_cache, json, re, random

requests_cache.install_cache('wikiGraph_cache')
# TODO: try catches
# TODO: article case sensitivity
# TODO: ignore files
# TODO: make the graphs look better than a firework
# TODO: make parser actually traverse redirects
# TODO: make each node in order 1 be a unique color, then order 2 to be that same color with less saturation; if they're connected to multiple nodes of order 1, then color them an average color?

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

def getWikiConnections(articleName):
		
	wikiURL = "https://en.wikipedia.org/w/api.php?action=query&rvprop=content&prop=revisions&rvsection=0&format=json&titles="
	#wikiURL = "https://en.wikipedia.org/w/api.php?action=query&rvprop=content&prop=revisions&format=json&titles="
	
	request = requests.get(wikiURL + articleName)
	article = request.json()
	try:
		articleText = article['query']['pages'][list(article['query']['pages'].keys())[0]]['revisions'][0]['*']
	except KeyError as e:
		print(e)
		return []
	
	#someKindofRegex = '\\[\\[([()A-z0-9 .,\'"]+)[\|]?([()A-z0-9 .,"\']+)?\\]\\]'
	someKindofRegex = '\\[\\[([()A-z0-9 .,\'\"]*?)(?:\|([()A-z0-9 .,\'\"]*?))?\\]\\]'
	searches = re.findall(someKindofRegex,articleText)
	connections = []
	#graph = graphviz.Digraph(comment='Connected Articles')
	#graph.node(articleName)
	
	for result in searches:
		connections.append((str(articleName), str(result[0])))
		#graph.edge(articleName, result[0])
	return connections
	
# load wiki page

if __name__ == '__main__':
	if len(sys.argv) > 1:
		articleName = sys.argv[1]
	
	graph = nx.DiGraph()
	# add main article as the 0th order 
	graph.add_node(articleName,order=0)
	mainConnections = list(set(getWikiConnections(articleName)))
	for connection in mainConnections:
		if connection[1] not in graph.nodes():
			graph.add_node(connection[1],order=1)
	print(mainConnections)
	graph.add_edges_from(list(mainConnections))
	print("Total unique connections: " + str(len(mainConnections)))
	secondaryConenctions = []
	for connection in mainConnections:
		print("Getting connections of article " + connection[1])
		secondaryNeighbors = list(set(getWikiConnections(connection[1])))
		print("  Unique connections: " + str(len(secondaryNeighbors)))
		secondaryConenctions.append(secondaryNeighbors)

	for connection in secondaryConenctions:
		for tertiaryConnection in connection:
			if tertiaryConnection[1] not in graph.nodes():			
				print (tertiaryConnection)
				graph.add_node(tertiaryConnection[1],order=2)
		try:
			graph.add_edges_from(connection)
		except Exception as e:
			print(e)
			
	print(graph.nodes())
	for node in graph.nodes():
		if not 'order' in graph.node[node].keys():
			graph.node[node]['order'] = 3
	#graph.render(filename='wikiGraphs/'+articleName)
	plt.figure(num=None, figsize=(75, 75), dpi=90)
	d = nx.degree(graph)
	color_map = {0:'#FF0000', 1:'#FF6600', 2:'#FFFF00', 3:'#CCCCCC'} 
	#node_sizes = [v * 250 for v in d.values()]
	#nodelist, node_sizes = zip(*node_sizes.items())
	pos = nx.spring_layout(graph)
	nx.draw(graph,pos,node_size=1200,node_shape='o',node_color='0.75', edgelist = [])
	nx.draw_networkx_nodes(graph, 
			cmap=plt.get_cmap('jet'), 
			node_color=[color_map[graph.node[node]['order']] for node in graph], 
			node_size=4000, 
			#with_labels=True,
			pos=pos)
	nx.draw_networkx_edges(graph,alpha=0.3,pos=pos)
	nx.draw_networkx_labels(graph,pos=pos)
	
	#nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph), labels=node_labels)
	#plt.show()
	print
	plt.savefig("wikiGraphs/" + articleName + ".png")
	