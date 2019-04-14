import sqlite3
from discord.ext import commands


class Users(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(name='score',
                description="Get a persons score.",
                pass_context=True)
    async def score(self, context, *args):
        try:
            if len(args) < 1:
                await context.message.channel.send('Give me a user to work with man...')
            else:
                await context.message.channel.send(get_users_score(args[0]))
        except Exception as e:
            await context.message.channel.send('Could not get that score')
            print(e)

def refresh_users(client):
    try:
        users = get_users()
        for guild in client.guilds:
            for member in guild.members:
                membername = '@' + member.name
                memberid = '<@' + str(member.id) +'>'
                if membername not in users:
                    conn = sqlite3.connect('quotes.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO users VALUES (?,?)", (membername,0,))
                    conn.commit()
                    conn.close()
                if memberid not in users:
                    conn = sqlite3.connect('quotes.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO users VALUES (?,?)", (memberid,0,))
                    conn.commit()
                    conn.close()
    except Exception as e:
        print(e)


def get_users():
    try:
        conn = sqlite3.connect('quotes.db')
        c = conn.cursor()
        c.execute("SELECT user FROM users")
        result = c.fetchall()
        conn.close()
        user = []
        for users in result:
            user.append(users[0])
        return user
    except Exception as e:
        print(e)

# TODO: Make work
def get_users_score(args):
    try:
        conn = sqlite3.connect('quotes.db')
        c = conn.cursor()
        c.execute("SELECT score FROM users WHERE user = (?)", (args,))
        result = c.fetchall()
        conn.close()
        scores = []
        for users in result:
            scores.append(users[0])
        return scores
    except Exception as e:
        print(e)

def setup(client):
    client.add_cog(Users(client))

