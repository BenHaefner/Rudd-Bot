import asyncio, config, discord, sqlite3, datetime, analytics
import cogs.users as users
from discord import Game
from discord.ext.commands import Bot
from threading import Lock


BOT_PREFIX = ("$")
TOKEN = config.Token()

client = Bot(command_prefix=BOT_PREFIX)

startup_extensions = ['quote', 'users', 'task', 'admin', 'analyze', 'inventory','money']

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
        if(before.id != 266162291735658496):
            with member_lock:
                global last_updated_member
                if(before.activity is not None):
                    previous_activity = analytics.check_last_activity_time(before.id)
                    timestamp = datetime.datetime.strptime(previous_activity[2], '%Y-%m-%d %H:%M:%S.%f')
                    if(type(before.activity) is not discord.Spotify and type(last_updated_member.activity) is not discord.Spotify or type(before.activity) is not discord.Streaming and type(last_updated_member.activity) is not discord.Streaming):
                        if(last_updated_member.name != before.name or last_updated_member.activity.name != before.activity.name):
                            if(previous_activity[1] == before.activity.name and (datetime.datetime.now() - timestamp) > datetime.timedelta(minutes=120) or previous_activity[1] != before.activity.name):
                                if(type(before.activity) is discord.Game):
                                    if(analytics.check_for_game(before.activity.name)):
                                        analytics.update_game(before.activity.name)
                                    else:
                                        analytics.insert_new_game(before.activity.name)
                                elif(type(before.activity) is discord.Activity):
                                    if(analytics.check_for_game(before.activity.name)):
                                        analytics.update_game(before.activity.name)
                                    else:
                                        analytics.insert_new_game(before.activity.name)
                            analytics.delete_and_insert_last_played(before.id, before.activity.name)
                    if(type(before.activity) is discord.Spotify and type(last_updated_member.activity) is discord.Spotify):
                        if(before.activity.title != last_updated_member.activity.title):
                            if(previous_activity[1] == before.activity.title and (datetime.datetime.now() - timestamp) > datetime.timedelta(minutes=120) or previous_activity[1] != before.activity.title):
                                if(analytics.check_for_song(before.activity.title,before.activity.artist)):
                                    analytics.update_song(before.activity.title,before.activity.artist)
                                else:
                                    analytics.insert_new_song(before.activity.title,before.activity.artist)
                            analytics.delete_and_insert_last_played(before.id, before.activity.title)
                    elif(type(before.activity) is discord.Spotify):
                        if(previous_activity[1] == before.activity.title and (datetime.datetime.now() - timestamp) > datetime.timedelta(minutes=120) or previous_activity[1] != before.activity.title):
                            if(analytics.check_for_song(before.activity.title,before.activity.artist)):
                                analytics.update_song(before.activity.title,before.activity.artist)
                            else:
                                analytics.insert_new_song(before.activity.title,before.activity.artist)
                        analytics.delete_and_insert_last_played(before.id, before.activity.title)
                    last_updated_member = before
    except Exception as e:
        analytics.delete_and_insert_last_played(before.id, before.activity.name)
        last_updated_member = before
        print(e)

for extension in startup_extensions:
    try:
        client.load_extension('cogs.' + extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(TOKEN)
