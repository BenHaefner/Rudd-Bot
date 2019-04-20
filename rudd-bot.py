import asyncio, config, discord, sqlite3
import cogs.users as users
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("$")
TOKEN = config.Token()

client = Bot(command_prefix=BOT_PREFIX)

startup_extensions = ["quote", "users", "task", "admin"]

@client.event
async def on_ready():
    await client.change_presence(activity=Game(name='Bobby Newport in P&R'))
    print('Logged in as ' + client.user.name)
    users.refresh_users(client)

@client.event
async def on_member_join(member):
    await member.edit(nick = 'Unkown (' + member.name + ')')
    await member.guild.text_channels[0].send('Hey there! I changed your nickname. This' + 
    ' server has a strict nicknaming policy to avoid confusion. The format is "FirstName LastInitial (Username)"')
    users.refresh_users(client)


for extension in startup_extensions:
    try:
        client.load_extension('cogs.' + extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(TOKEN)
