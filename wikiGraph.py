#!/usr/bin/python3

import sys, os, requests, requests_cache, json, re, random

requests_cache.install_cache('wikiGraph_cache')
# TODO: try catches
# TODO: article case sensitivity
# TODO: ignore files
# TODO: make the graphs look better than a firework
# TODO: make parser actually traverse redirects
# TODO: make each node in order 1 be a unique color, then order 2 to be that same color with less saturation; if they're connected to multiple nodes of order 1, then color them an average color?
# TODO: keyword density based edge weights and therefore a better fucking graph display

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

import graphviz
from networkx.drawing.nx_agraph import graphviz_layout

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def getWikiConnections(articleName, getAll=False):
		
	wikipedia = "https://en.wikipedia.org/w/"
	awoiaf = "http://awoiaf.westeros.org/"
	if not getAll:
		apicall = "api.php?action=query&rvprop=content&prop=revisions&rvsection=0&format=json&titles="
	else:
		apicall = "api.php?action=query&rvprop=content&prop=revisions&format=json&titles="
	wikiURL = wikipedia + apicall
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
	graph.add_node(articleName,order=0,pos=(0,0))
	mainConnections = getWikiConnections(articleName, getAll=False)
	weight = 0
	for connection in mainConnections:
		if connection[1] not in graph.nodes():
			graph.add_node(connection[1],order=1,distance=1-(weight/len(list(set(mainConnections)))))	
			weight += 1
	print(mainConnections)
	for connection in mainConnections:
		#tempTuple = (connection + (graph.node[connection[1]]['distance'],))
		#print(tempTuple)
		graph.add_edge(connection[0], connection[1], weight=graph.node[connection[1]]['distance'])
	print("Total unique connections: " + str(len(mainConnections)))
	
	for connection in mainConnections:
		secondaryConnections = []
		print("Getting connections of article " + connection[1])
		secondaryConnections = getWikiConnections(connection[1])
		print("  Unique connections: " + str(len(list(set(secondaryConnections)))))		
		print(secondaryConnections)
		weight = 0
		for subConnection in secondaryConnections:
			print(subConnection)
			if subConnection[1] not in graph.nodes():			
				graph.add_node(subConnection[1],order=2,)
				distance = 1-weight/len(list(set(secondaryConnections)))
				weight += 1
				try:
					graph.add_edge(subConnection[0], subConnection[1], weight=distance)
				except Exception as e:
					continue
			
			
	print(graph.nodes())
	for node in graph.nodes():
		if not 'order' in graph.node[node].keys():
			graph.node[node]['order'] = 3
	#graph.render(filename='wikiGraphs/'+articleName)
	plt.figure(num=None, figsize=(75, 75), dpi=90)
	d = nx.degree(graph)
	color_map = {0:'#FF0000', 1:'#FF6600', 2:'#FFFF00', 3:'#CCCCCC'} 
	print("Total nodes: " + str(len(graph.nodes())))
	#node_sizes = [v * 250 for v in d.values()]
	#nodelist, node_sizes = zip(*node_sizes.items())
	#fixed_pos = {articleName:(0.5,0.5)}
	#fixed_nodes = fixed_pos.keys()
	#pos = nx.spring_layout(graph, pos=fixed_pos, fixed=fixed_nodes)
	shells = []
	for i in range(0,3):
		shells.append(list(n for n in graph if graph.node[n]['order']==i))
	print(shells)
	pos = nx.spring_layout(graph, iterations=50, weight=1)#, pos=fixed_pos, fixed=fixed_nodes)
	# pos = nx.shell_layout(graph,shells)
	#print(pos)
	#pos[articleName] = [0.5,0.5]
	nx.draw(graph,pos,node_size=4000,node_shape='o',node_color='0.75', edgelist = [])
	nx.draw_networkx_nodes(graph, 
			cmap=plt.get_cmap('jet'), 
			node_color=[color_map[graph.node[node]['order']] for node in graph], 
			node_size=4000, 
			node_alpha=0.5,
			#with_labels=True,
			pos=pos)
	nx.draw_networkx_edges(graph,alpha=0.3,pos=pos)
	#nx.draw_networkx_edge_labels(graph,pos=pos)
	nx.draw_networkx_labels(graph,pos=pos)
	
	#nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph), labels=node_labels)
	#plt.show()
	print
	plt.savefig("wikiGraphs/" + articleName + ".png")
	