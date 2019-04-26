import discord, sqlite3
from discord.ext import commands

class Analyze(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(name='songs',
                description='Gets list of most played songs.',
                pass_context=True)
    async def songs(self, context):
        pass

    @commands.command(name='games',
                description='Gets list of most played games.',
                pass_context=True)
    async def games(self, context):
        pass

def setup(client):
    client.add_cog(Analyze(client))
