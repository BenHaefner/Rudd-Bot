import discord, sqlite3, analytics
from discord.ext import commands

class Analyze(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(name='songs',
                description='Gets list of most played songs.',
                pass_context=True)
    async def songs(self, context):
        try:
            top_five = top_songs()
            to_send = ''
            for item in top_five:
                to_send += item[0] + ' by ' + item[1] + ': ' + str(item[2]) + '\n'
            await context.message.channel.send(to_send)
        except Exception as e:
            await context.message.channel.send("Something went wrong")
            print(e)

    @commands.command(name='games',
                description='Gets list of most played games.',
                pass_context=True)
    async def games(self, context):
        try:
            top_five = top_games()
            to_send = ''
            for item in top_five:
                to_send += item[0] + ': ' + str(item[1]) + '\n'
            await context.message.channel.send(to_send)
        except Exception as e:
            await context.message.channel.send("Something went wrong")
            print(e)

    @commands.command(name='ban',
                    description='Ban a game from appearing in analytics',
                    pass_context=True)
    async def ban(self, context, *args):
        try:
            msg = ' '.join(args)
            await context.message.channel.send(ban_game(msg))
        except Exception as e:
            await context.message.channel('Couldnt ban for some reason.')
            print(e)

def top_games():
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM played_games ORDER BY count DESC LIMIT 5')
    result = c.fetchall()
    conn.close()
    return result

def top_songs():
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM played_songs ORDER BY count DESC LIMIT 5')
    result = c.fetchall()
    conn.close()
    return result

def ban_game(game):
    try:
        returnable = "The game already exists in the banned list."
        banned = analytics.get_banned()
        if(game not in banned):
            conn = sqlite3.connect('rudd.db')
            c = conn.cursor()
            c.execute('INSERT INTO banned_games VALUES (?)', (game,))
            conn.commit()
            conn.close()
            returnable = "Banned."
        return returnable
    except Exception as e:
        print(e)

def setup(client):
    client.add_cog(Analyze(client))
