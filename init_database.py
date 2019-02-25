import sqlite3
conn= sqlite3.connect("actors.db");
c=conn.cursor();
c.execute('''CREATE TABLE actors (name text,id real,bacon_number real)''');
conn.commit();
conn.close()