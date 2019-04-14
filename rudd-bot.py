import asyncio, config, discord, sqlite3
import cogs.users as users
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("$")
TOKEN = config.Token()

client = Bot(command_prefix=BOT_PREFIX)

startup_extensions = ["quote"]

@client.event
async def on_ready():
    await client.change_presence(activity=Game(name=" Bobby Newport in P&R"))
    print("Logged in as " + client.user.name)
    users.refresh_users(client)
        

for extension in startup_extensions:
    try:
        client.load_extension('cogs.' + extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(TOKEN)
