import urllib
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3

def ActorNumber(n):
	str_num=str(n);
	
	return "0"*(8-len(str_num))+str_num;
	


def find_time(soup):
	times=soup.find_all("time");
	birthplace=None;
	deathplace=None;
	birthtime=None;
	deathtime=None;

	if len(times) !=0:
		birthtime=times[0]["datetime"];
		if(len(times)>1):
			deathtime=times[1]["datetime"];
	#print(birthtime,deathtime);
	
	places=soup.find_all("a",href=True);
	
	for place in places:
		if "birth_place" in place['href']:
			birthplace=place.string;
		if "death_place" in place["href"]:
			deathplace=place.string;

	#print(birthplace,deathplace);
	
	return birthtime,deathtime,birthplace,deathplace
	
	


		
conn= sqlite3.connect("actors.db");
c=conn.cursor();

i=3020;
max_len=0;
while True:
	try:
		url="https://www.imdb.com/name/nm"+ActorNumber(i)+"/?ref_=nmls_hd";
		response=urlopen(url);
		html=response.read();
		soup=BeautifulSoup(html,'html.parser');
		name=soup.find_all("span",class_="itemprop",limit=1)[0].string;
		birthname,deathtime,birthplace,deathplace=find_time(soup);
		print(name,birthname,deathtime,birthplace,deathplace,i);
		c.execute('INSERT INTO actors VALUES (?,?,?,?,?,?,?)',(birthname,deathtime,i, name,None,birthplace,deathplace))
		i=i+1;
		conn.commit()
	except:
		break;
conn.close();