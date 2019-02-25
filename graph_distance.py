import heapq;
import json
import sqlite3

class priority_queque:
	def __init__(self,h=None):
		self.heap=[];
		if h==None:
			heap=[];
		else:
			heap=h;
	
	def push(self,item):
		heapq.heappush(heap,item);
	def pop(self):
		return heapq.heappop(heap);
	def isEmpty(self):
		return len(heap)==0;
	
with open("graph.json")as load_graph:
	graph=json.load(load_graph);
	
	distances={};
	
	heap=[[0,"Kevin Bacon0000102"]];

	node_queque=priority_queque(heap);
	
	while(node_queque.isEmpty()== False):
		cinema=node_queque.pop();
		if(not cinema[1] in distances): 
			distances[cinema[1]]=cinema[0];
			#print(cinema[1],cinema[0]);
			if cinema[1] in graph:
				neighbors=graph[cinema[1]];
				
				for item in neighbors:
					if not item in node_queque.heap:
						node_queque.push([cinema[0]+1,item]);
					
			
		else:
			if distances[cinema[1]]> cinema[0]:
				distances[cinema[1]]=cinema[0];
			else:
				continue;
		
		
	conn = sqlite3.connect('actors.db');
	c = conn.cursor();
	for k,v in distances.items():
		if v%2==0:
			name=k[:len(k)-7];
			id=k[len(k)-7:];
			distance=v/2;
			print(name,id,distance);
			c.execute("INSERT INTO actors VALUES (?,?,?)",(name,id,distance));
			
		
	for i in c.execute("SELECT Count(*) FROM actors"):
		print(i);
	
	
	
	
	
		
		