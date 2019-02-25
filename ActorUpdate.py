import sqlite3
import urllib
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

def ActorNumber(n):
	str_num=str(n);
	return "0"*(8-len(str_num))+str_num;

def rank(id):
		
		ratings=[];
		
		url="https://www.imdb.com/name/nm"+ActorNumber(id)+"/?ref_=nmls_hd";
		response=urlopen(url);
		html=response.read();
		soup=BeautifulSoup(html,'html.parser');
		sum=0;
		length=0;
		
		for link in soup.find_all("div",class_="filmo-row odd"):
			
			for item in link.find_all("a",href=True):
				#print(item["href"]);
				try:
					if "title/" in item["href"]:
						url_="https://www.imdb.com"+item["href"]
						#print(link.string);
						response_=urlopen(url_);
						html_=response_.read();
						soup_=BeautifulSoup(html_,'html.parser');
						for rating in soup_.find_all("span",itemprop="ratingValue"):
							print(rating.string);
							sum+=float(rating.string);
							length+=1;
				except:
					continue;
		
		
		return sum/length;
		
conn= sqlite3.connect("actors.db");
c=conn.cursor();
actor_list=[];

for actor in c.execute('''SELECT * FROM actors'''):
	print(actor[3]);
	actor_list.append([]);
	id=int(actor[2]);
	ranks=rank(id);
	actor_list.append([ranks,id]);
c.executemany("""UPDATE actors SET rank=? WHERE id=?""",actor_list);
conn.commit();

conn.close()