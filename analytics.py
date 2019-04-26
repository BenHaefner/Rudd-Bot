import discord, sqlite3, datetime

def delete_and_insert_last_played(id, title):
    id = '<@' + str(id) + '>'
    id = id.replace('!','')
    now = datetime.datetime.now()
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('DELETE FROM played_activity WHERE id = ?',(id,))
    c.execute('INSERT INTO played_activity VALUES (?,?,?)',(id,title,now,))
    conn.commit()
    conn.close()

def check_last_activity_time(id):
    id = '<@' + str(id) + '>'
    id = id.replace('!','') 
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM played_activity WHERE id = ?',(id,))
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result

def insert_new_song(title, artist):
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('INSERT INTO played_songs VALUES (?,?,?)',(title,artist,1,))
    conn.commit()
    conn.close()

def insert_new_game(name):
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('INSERT INTO played_games VALUES (?,?)',(name,1,))
    conn.commit()
    conn.close()

def update_song(title, artist):
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('UPDATE played_songs SET count = count + 1 WHERE title = ? AND artist = ?',(title, artist,))
    conn.commit()
    conn.close()

def update_game(game):
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('UPDATE played_games SET count = count + 1 WHERE name = ? ',(game,))
    conn.commit()
    conn.close()

def check_for_game(name):
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM played_games WHERE name = ?',(name,))
    result = c.fetchone()
    conn.close()
    if result is None:
        return False
    else:
        return True

def check_for_song(title, artist):
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM played_songs WHERE title = ? AND artist = ?',(title,artist,))
    result = c.fetchone()
    conn.close()
    if result is None:
        return False
    else:
        return True
