import discord, sqlite3, datetime

def delete_and_insert(id, title):
    id = '<@' + str(id) + '>'
    id = id.replace('!','')
    now = datetime.datetime.now()
    import sqlite3
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('DELETE FROM played_activity WHERE id = ?',(id,))
    c.execute('INSERT INTO played_activity VALUES (?,?,?)',(id,title,now,))
    conn.commit()
    conn.close()

def check_last_game_time(id):
    id = '<@' + str(id) + '>'
    id = id.replace('!','') 
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM played_activity WHERE id = ?',(id,))
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result
