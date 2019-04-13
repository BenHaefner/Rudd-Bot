import asyncio
import discord
import random
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands
import config

BOT_PREFIX = ("$")
TOKEN = config.Token

client = Bot(command_prefix=BOT_PREFIX)


@client.command(name='grab',
                description="Saves a quote.",
                brief="Answers from the beyond.",
                aliases=['yoink'],
                pass_context=True)
async def grab(context):
    msg = context.message.content + "\n"
    msg = msg.replace("$grab ", "")
    with open("quotes.txt", 'a') as myfile:
        myfile.write(msg)
    await client.say('Quote saved')

@client.command(name='quote',
                description="Get a quote.",
                brief="",
                pass_context=True)
async def quote(context):
    with open("quotes.txt", 'r') as myfile:
        msgArray = []
        for line in myfile:
            msgArray.append(line)
        msg = msgArray[random.randint(0, len(msgArray)-1)]
        await client.say(msg)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name=" Bobby Newport in P&R"))
    print("Logged in as " + client.user.name)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)