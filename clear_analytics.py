import sqlite3

conn = sqlite3.connect('Rudd-Bot/rudd.db')
c = conn.cursor()
c.execute('DELETE FROM played_games')
c.execute('DELETE FROM played_songs')
conn.commit()
conn.close()