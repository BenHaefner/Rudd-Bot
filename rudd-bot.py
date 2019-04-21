import asyncio, config, discord, sqlite3, datetime
import cogs.users as users
from discord import Game
from discord.ext.commands import Bot
from threading import Lock


BOT_PREFIX = ("$")
TOKEN = config.Token()

client = Bot(command_prefix=BOT_PREFIX)

startup_extensions = ["quote", "users", "task", "admin"]

last_updated_member = discord.Member
member_lock = Lock()

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

@client.event
async def on_member_update(before, after):
    try:
        with member_lock:
            global last_updated_member
            if(before.activity is not None):
                if(type(before.activity) is not discord.Spotify and type(last_updated_member.activity) is not discord.Spotify or type(before.activity) is not discord.Streaming and type(last_updated_member.activity) is not discord.Streaming):
                    if(last_updated_member.name != before.name or last_updated_member.activity.name != before.activity.name):
                        if(type(before.activity) is discord.Game):
                            print(before.name + ': ' + before.activity.name + ' ' + str(datetime.datetime.now()))
                        elif(type(before.activity) is discord.Activity):
                            print(before.name + ': ' + before.activity.name + ' ' + str(datetime.datetime.now()))
                        else:
                            print(before.activity)
                if(type(before.activity) is discord.Spotify and type(last_updated_member.activity) is discord.Spotify):
                    if(before.activity.title != last_updated_member.activity.title):
                        print(before.name + ': ' + before.activity.title + ' ' + str(datetime.datetime.now()))
                elif(type(before.activity) is discord.Spotify):
                    print(before.name + ': ' + before.activity.title + ' ' + str(datetime.datetime.now()))
                last_updated_member = before
    except Exception as e:
        last_updated_member = before
        print(e)

for extension in startup_extensions:
    try:
        client.load_extension('cogs.' + extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(TOKEN)
