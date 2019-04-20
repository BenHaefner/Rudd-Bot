import random, re, discord, sqlite3, cogs.users
from discord.ext import commands

# Database: rudd.db
# Tables: quotes, users
# User column: user
# Quote column: quote


class Quote(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.members = cogs.users.get_users()
        cogs.users.refresh_users(client)

    @commands.command(name='grab',
                description='Saves the last message send.',
                pass_context=True)
    async def grab(self, context):
        try:
            self.members = cogs.users.get_users()
            msg = context.message
            onNext = False
            history = await context.message.channel.history().flatten()
            for i, message in enumerate(history):
                if onNext is True:
                    author = str(message.author.id)
                    args = '<@' + author + '> ' + message.content.replace('grab ', '')
                    await context.message.channel.send(addQuote(self.members,args))
                    break
                if message.id == msg.id:
                    onNext = True
        except Exception as e:
            await context.message.channel.send('Quote could not be saved')
            print(e)


    @commands.command(name='quote',
                    description='Get a quote, or quote a user.',
                    pass_context=True)
    async def quote(self, context, *args):
        try:
            self.members = cogs.users.get_users()
            if (len(args) is 0):
                await context.message.channel.send(getRandQuote())
            else:
                msg = ' '.join(args)
                await context.message.channel.send(addQuote(self.members,msg))
        except Exception as e:
            await context.message.channel('You are doing something unsafe. If you have an apostraphy or quotation mark... I dont like that shit.')
            print(e)
    
    @commands.command(name='lookup',
                description='Gets a users quote.',
                pass_context=True)
    async def lookup(self, context, args):
        try:
            self.members = cogs.users.get_users()
            if (len(args) is None):
                await context.message.channel.send('Specify a user to lookup a quote for.')
            else:
                await context.message.channel.send(getRandQuoteOfUsers(self.members,args))
        except Exception as e:
            await context.message.channel.send('Something went wrong')
            print(e)


def addQuote(members, args):
    user = args.split()[0].strip().replace('!','')
    if "@" not in user:
        return 'Quote could not be added, please include a user'
    if user not in members:
        return 'That is not currently a member of this or any server I know.'
    conn = sqlite3.connect('rudd.db')
    message = '"' + ' '.join(args.split()[1:]) + '"'
    q = (user,message)
    c = conn.cursor()
    c.execute('INSERT INTO quotes VALUES (?,?)', q)
    conn.commit()
    conn.close()
    return 'Quote added.'


def getRandQuote():
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * From quotes')
    result = c.fetchall()
    result = result[random.randint(0, len(result) - 1)]
    name = cogs.users.get_name_from_id(result[0])
    message = ' '.join(result[1:])
    result = name + ": " + message
    conn.close()
    return result 


def getRandQuoteOfUsers(members, args):
    args = args.replace('!','')
    if "@" not in args:
        return 'That isnt a user!'
    if args not in members:
        return 'That is not currently a member of this or any server I know.'
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * From quotes WHERE user = (?)', (args,))
    result = c.fetchall()
    result = result[random.randint(0, len(result) - 1)]
    name = cogs.users.get_name_from_id(result[0])
    message = ' '.join(result[1:])
    result = name + ": " + message
    conn.close()
    return result

def set_users(users):
    pass

def setup(client):
    client.add_cog(Quote(client))

