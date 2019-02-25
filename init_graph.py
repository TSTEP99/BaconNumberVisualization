import sqlite3
conn= sqlite3.connect("graph.db");
c=conn.cursor();
c.execute('''CREATE TABLE node (id integer, name text,url text)''');
conn.commit();
conn.close()