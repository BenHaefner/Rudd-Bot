import asyncio, config, discord, sqlite3, datetime, analytics
import cogs.users as users
from discord import Game
from discord.ext.commands import Bot
from threading import Lock

# Set prefix for bot commands to $
BOT_PREFIX = ("$")
TOKEN = config.Token()
# Create client
client = Bot(command_prefix=BOT_PREFIX)
# List of the files to run as extensions
startup_extensions = ['quote', 'users', 'task', 'admin', 'analyze', 'inventory','money']
# Instantiate global variables, and mutex
last_updated_member = discord.Member
member_lock = Lock()
# Output ready message
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name='Bobby Newport in P&R'))
    print('Logged in as ' + client.user.name)
    # Refresh user list 
    users.refresh_users(client)
# Change member name to conform with server standards.
@client.event
async def on_member_join(member):
    await member.edit(nick = 'Unkown (' + member.name + ')')
    await member.guild.text_channels[0].send('Hey there! I changed your nickname. This' + 
    ' server has a strict nicknaming policy to avoid confusion. The format is "FirstName LastInitial (Username)"')
    users.refresh_users(client)
# Server Analytics
@client.event
async def on_member_update(before, after):
    try:
        # Ignore a bot which outputs its activity too often
        # TODO: Find a way to ignore users without needed to hardcode them. Probably by storing their name in a database or file.
        if(before.id != 266162291735658496):
            # Use mutex to stop multiple accidental firings from affecting results
            with member_lock:
                global last_updated_member
                if(before.activity is not None):
                    # Get last activity and timestamp for ensuring that the last activity they 
                    # launched is not the same as this, or within a time window
                    previous_activity = analytics.check_last_activity_time(before.id)
                    timestamp = datetime.datetime.strptime(previous_activity[2], '%Y-%m-%d %H:%M:%S.%f')
                    # Check if activity is not a spotify activity, or streaming.
                    if(type(before.activity) is not discord.Spotify and type(last_updated_member.activity) is not discord.Spotify or type(before.activity) is not discord.Streaming and type(last_updated_member.activity) is not discord.Streaming):
                        # Check that the activity or the last user is not the same as the last.
                        if(last_updated_member.name != before.name or last_updated_member.activity.name != before.activity.name):
                            # Ensure that the launching is not within the hour and a half window
                            if(previous_activity[1] == before.activity.name and (datetime.datetime.now() - timestamp) > datetime.timedelta(minutes=120) or previous_activity[1] != before.activity.name):
                                # Update the activity list
                                if(before.activity.name.lower() not in analytics.get_banned()):
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
                            # Update last played game for user
                            analytics.delete_and_insert_last_played(before.id, before.activity.name)
                    # Because discord.py's nortmal activity API doesnt have a 'title' function , 
                    # the elif block is necessary to properly record spotify song plays if last acticity isnt spotify.
                    if(type(before.activity) is discord.Spotify and type(last_updated_member.activity) is discord.Spotify):
                        # Check the song is different from the previous song.
                        if(before.activity.title != last_updated_member.activity.title):
                            # Ensure that the playing is not within the hour and a half window
                            if(previous_activity[1] == before.activity.title and (datetime.datetime.now() - timestamp) > datetime.timedelta(minutes=120) or previous_activity[1] != before.activity.title):
                                # Update database
                                if(analytics.check_for_song(before.activity.title,before.activity.artist)):
                                    analytics.update_song(before.activity.title,before.activity.artist)
                                else:
                                    analytics.insert_new_song(before.activity.title,before.activity.artist)
                            # Update last played song for user
                            analytics.delete_and_insert_last_played(before.id, before.activity.title)
                    elif(type(before.activity) is discord.Spotify):
                        # Ensure that the playing is not within the hour and a half window
                        if(previous_activity[1] == before.activity.title and (datetime.datetime.now() - timestamp) > datetime.timedelta(minutes=120) or previous_activity[1] != before.activity.title):
                            # Update database
                            if(analytics.check_for_song(before.activity.title,before.activity.artist)):
                                analytics.update_song(before.activity.title,before.activity.artist)
                            else:
                                analytics.insert_new_song(before.activity.title,before.activity.artist)
                            # Update last played song for user
                        analytics.delete_and_insert_last_played(before.id, before.activity.title)
                    # Update last updated member
                    last_updated_member = before
    except Exception as e:
        # Print error message for owner. Update user
        analytics.delete_and_insert_last_played(before.id, before.activity.name)
        last_updated_member = before
        print(e)
# Load extensions
for extension in startup_extensions:
    try:
        client.load_extension('cogs.' + extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))
# Run the bot
client.run(TOKEN)
