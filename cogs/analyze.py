import discord, sqlite3
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
            for item in top_five:
                await context.message.channel.send(item[0] + ' by ' + item[1] + ': ' + str(item[2]))

        except Exception as e:
            await context.message.channel.send("Something went wrong")
            print(e)

    @commands.command(name='games',
                description='Gets list of most played games.',
                pass_context=True)
    async def games(self, context):
        try:
            top_five = top_games()
            for item in top_five:
                await context.message.channel.send(item[0] + ': ' + str(item[1]))

        except Exception as e:
            await context.message.channel.send("Something went wrong")
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

def setup(client):
    client.add_cog(Analyze(client))
