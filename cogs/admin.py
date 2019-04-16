import random, re, discord, sqlite3, cogs.users
from discord.ext import commands

# Database: rudd.db
# Tables: quotes, users
# User column: user
# Quote column: quote


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.members = cogs.users.get_users()
        cogs.users.refresh_users(client)

    @commands.command(name='pin',
                description="Pins a message.",
                pass_context=True)
    async def pin(self, context):
        try:
            msg = context.message
            onNext = False
            history = await msg.channel.history().flatten()
            for i, message in enumerate(history):
                if onNext is True:
                    await message.pin()
                    await context.message.channel.send("Message has been pinned!")
                    break
                if message.id == msg.id:
                    onNext = True
        except Exception as e:
            await context.message.channel.send('Could not pin message')
            print(e)

def setup(client):
    client.add_cog(Admin(client))

