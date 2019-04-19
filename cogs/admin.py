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

    @commands.command(name='commands',
                description="Print list of commands.",
                pass_context=True)
    async def pin(self, context):
        try:
            texts = commands_text
            for text in texts:
                await context.message.channel.send(text)
        except Exception as e:
            await context.message.channel.send('Could not get commands')
            print(e)

def commands_text():
    return ['Every command is proceeded by a "$"'
        , 'quote: Gets a random quote'
        , 'quote -mention- -message-: Quotes a user'
        , 'grab: Adds the last message as a quote'
        , 'lookup -mention-: Lookup a random quote from metioned user.'
        , 'score -mention-: Retrieves score of mentioned user.'
        , '++ -mention-: Increases mentioned user score'
        , '-- -mention-: Decreases mentioned user score'
        , 'scores: Lists all scores'
        , 'add_task -keyword- -text-: Adds a task accessible through the keyword'
        , 'lookup_task -keyword-: Gets text associated with keyword'
        , 'list_tasks: Lists all keywords of tasks'
        , 'end_task -keyword-: Deletes task associated with keyword'
        , 'pin: Pins the last comment']

def setup(client):
    client.add_cog(Admin(client))

