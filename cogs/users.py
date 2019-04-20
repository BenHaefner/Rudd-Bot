import sqlite3
from discord.ext import commands

# Database: rudd.db
# Tables: users
# cloumns: user, score, name


class Users(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(name='score',
                description='Get a persons score.',
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

    @commands.command(name='++',
                description='Increase a persons score.',
                pass_context=True)
    async def inc(self, context, *args):
        try:
            if len(args) < 1:
                await context.message.channel.send('Give me a user to work with man...')
            else:
                id = '<@' + str(context.message.author.id) + '>'
                if id == str(args[0]):
                    await context.message.channel.send('Hey man, dont increase your own score. Not cool...')
                    return
                await context.message.channel.send(increment(args[0]))
        except Exception as e:
            await context.message.channel.send('Could not get that score')
            print(e)
    
    @commands.command(name='--',
                description='Decrease a persons score.',
                pass_context=True)
    async def dec(self, context, *args):
        try:
            if len(args) < 1:
                await context.message.channel.send('Give me a user to work with man...')
            else:
                id = '<@' + str(context.message.author.id) + '>'
                if id == str(args[0]):
                    await context.message.channel.send('Hey man, dont increase your own score. Have confidence!')
                    return
                await context.message.channel.send(decrement(args[0]))
        except Exception as e:
            await context.message.channel.send('Could not get that score')
            print(e)

    @commands.command(name='scores',
                description='Get all scores.',
                pass_context=True)
    async def scores(self, context):
        try:
            allScores = get_all_scores()
            for scores in allScores:
                if '<' in scores[0]:
                    await context.message.channel.send(str(scores[2]) + ': ' + str(scores[1]))
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
                if memberid not in users:
                    conn = sqlite3.connect('rudd.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO users VALUES (?,?,?)', (memberid,0,membername.replace('@','')))
                    conn.commit()
                    conn.close()
    except Exception as e:
        print(e)


def get_users():
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT user FROM users')
        result = c.fetchall()
        conn.close()
        user = []
        for users in result:
            user.append(users[0])
        return user
    except Exception as e:
        print(e)

def get_all_scores():
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        result = c.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(e)

def get_users_score(args):
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT score FROM users WHERE user = (?)', (args,))
        result = c.fetchone()
        conn.close()
        return result[0]
    except Exception as e:
        print(e)

def increment(args):
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT score FROM users WHERE user = (?)', (args,))
        result = int(c.fetchone()[0])
        result = result + 1
        c.execute('UPDATE users SET score = ? WHERE user = ?', (result, args,))
        conn.commit()
        conn.close()
        return 'The score of ' + str(args) + ' is ' + str(result)
    except Exception as e:
        print(e)

def decrement(args):
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT score FROM users WHERE user = (?)', (args,))
        result = int(c.fetchone()[0])
        result = result - 1
        c.execute('UPDATE users SET score = ? WHERE user = ?', (result, args,))
        conn.commit()
        conn.close()
        return 'The score of ' + str(args) + ' is ' + str(result)
    except Exception as e:
        print(e)

def get_name_from_id(id):
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT name FROM users WHERE user = (?)', (id,))
        result = c.fetchone()[0]
        conn.close()
        return result
    except Exception as e:
        print(e)
        return id



def setup(client):
    client.add_cog(Users(client))

