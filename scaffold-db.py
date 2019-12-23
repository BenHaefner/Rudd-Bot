import sqlite3

print("Beginning to scaffold Rudd-Bot Database....")
try:
    print("Creating file...")
    f = open("rudd.db","w+")
    f.close()
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    print("Creating tables...")
    c.execute("CREATE TABLE IF NOT EXISTS banned_games (title text)")
    c.execute("CREATE TABLE IF NOT EXISTS inventory (item text, quantity integer)")
    c.execute("CREATE TABLE IF NOT EXISTS money (type text, quantity integer)")
    c.execute("CREATE TABLE IF NOT EXISTS played_activity (id text, activity text, time timestamp)")
    c.execute("CREATE TABLE IF NOT EXISTS played_games (name text, count integer)")
    c.execute("CREATE TABLE IF NOT EXISTS played_songs (title text, artist text, count integer)")
    c.execute("CREATE TABLE IF NOT EXISTS quotes (user text, quote text)")
    c.execute("CREATE TABLE IF NOT EXISTS servers (server text)")
    c.execute("CREATE TABLE IF NOT EXISTS task (name text, description text)")
    c.execute("CREATE TABLE IF NOT EXISTS users (user text, score integer, name text)")
    conn.commit()
    conn.close()
except Exception as e:
    print(e)
