import urllib;
import pandas as pd;
from urllib.request import urlopen;
from bs4 import BeautifulSoup;
import sqlite3;
import json;


class queque:
	def __init__(self): #intilizes the list which the queque is implemented
		self.array=[];
	def pop(self):	#pop the first element
		item=self.array[0];
		del self.array[0];
		return item;
	def push(self,item): #pushes an element on the end
		self.array.append(item);
	def is_empty(self):	#return 0 if full 1 if the queque is empty
		if(len(self.array))==0:	#IS the array is empty returns 1
			return 1
		else:
			return 0; #returns 0 if otherwise
			

graph={};# gives actual graph to be displayed
url_queque= queque(); #makeas a queque for the links being searched.
url_checker={};# Makes sure url already visited is not visited again

with open('graph.json','r') as json_data: #makes sure to load previous json to help keep track of links placed in graph;
	graph=json.load(json_data);

#with open("url_checker.json","r") as json_data: #gets previous URLs that were checked
	#url_checker=json.load(json_data);


def is_integer(number):
	
	digits=[str(i) for i in range(10)]; #creates and array of 

	try:
		int(number)#Sees if it can be converyted to an integer
		return True
	except ValueError:
		return False #returns false if it cannot or true if it can

def find_name(soup,type):
	
	if type=="A": #Says is an actor being passed
		name=soup.find_all("span",class_="itemprop",limit=1);# finds the first item on the span tag of itemprop class
		name=name[0].string;
		return name;
	elif type=="M": #If movie being passed
		name=soup.select('h1')[0].text.strip(); #selects based on h1 tag
		if len(name)>=6 and name[-1]==')' and name[-6]=='(' and is_integer(name[-5:-1]):
			name=name[:len(name)-7];
		return name;

def find_movies(soup):
	
	edges=[] # list of edges to be used for the graph when returned
	
	global url_checker; # gives function acess to url related local variables
	global url_queque;
	
	for link in soup.select("div.filmo-row"): #selectes the movies in the rows
		for item in link.find_all("a",href=True,limit=1): # further slects the html with the a tag
			if item.string != None:
				id=item["href"][len("/title/tt"):len("/title/tt")+7]; #gives id to the name of movie
				edges.append(item.string+id);
				url="https://www.imdb.com"+item["href"];
				if not url in url_checker: # makes sure no movie that have already been visited are visited again
					url_queque.push(url); #pushes onto queque if not
					url_checker[url]=1;
					with open("url_checker.json","w") as json_data:
						json.dump(url_checker,json_data);
						json_data.truncate();
						
	return edges;
				

def find_actors(soup):
	edges=[]; #list of edges to be used for the graph when returned
	
	global url_checker;# allows local variables to be used
	global url_queque;

	for tag in soup.find_all("td",class_=None):
		for actor in tag.find_all("a",href=True,limit=1):#FInds the a tag enclosed inside the td
			if actor.string != None:
				id=actor["href"][len("/name/nm"):len("/name/nm")+7]; #gets the number from the href attribute
				edges.append(actor.string[:-1]+id);
				url="https://www.imdb.com"+actor["href"];
				if not url in url_checker:
					url_queque.push(url);
					url_checker[url]=1;
					with open("url_checker.json","w") as json_data:
						json.dump(url_checker,json_data);
						json_data.truncate();
					
		
	
	return edges;

		

def spider():
	global graph;
	global url_queque;
	
	while url_queque.is_empty()!=1: #Checks if queque is empyty or not
	
		try:
			url=url_queque.pop();
			response=urlopen(url);
			html=response.read();
			soup=BeautifulSoup(html,'html.parser');
		except:
			continue;
		
		
		
		
		if "https://www.imdb.com/name/" in url:
			name=find_name(soup,"A");
			name=name+url[len("https://www.imdb.com/name/nm"):len("https://www.imdb.com/name/nm")+7];#attaches the id to the name
			print(name)
			edges=find_movies(soup);
			#print(edges);
			graph[name]=edges;
			with open("graph.json","w") as json_data:
				json.dump(graph,json_data);
				json_data.truncate();
			
			
					
		elif "https://www.imdb.com/title/" in url:
			name=find_name(soup,"M");
			name=name+url[len("https://www.imdb.com/title/tt"):len("https://www.imdb.com/title/tt")+7];
			print(name)
			edges=find_actors(soup);
			#print(edges);
			graph[name]=edges;
			with open("graph.json","w") as json_data:
				json.dump(graph,json_data);
				json_data.truncate();

	

url="https://www.imdb.com/name/nm0000102";
url_queque.push(url);
url_checker[url]=1;
response=urlopen(url);
html=response.read();
soup=BeautifulSoup(html,'html.parser');
spider();

