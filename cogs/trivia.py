import sqlite3
import requests
from discord.ext import commands

class Trivia(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(name='trivia',
                description='Get a trivia question.',
                pass_context=True)
    async def score(self, context, *args):
        try:
            await context.message.channel.send(get_trivia_question())
        except Exception as e:
            await context.message.channel.send('Could not get a trivia question.')
            print(e)

def get_trivia_question():
    response = requests.get("https://opentdb.com/api.php?amount=1")
    print (response.json())

def setup(client):
    client.add_cog(Trivia(client))

