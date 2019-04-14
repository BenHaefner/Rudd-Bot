import random, re, discord, sqlite3, cogs.users
from discord.ext import commands

# Database: quotes.db
# Tables: quotes, users
# User column: user
# Quote column: quote


class Quote(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.members = cogs.users.get_users()
        cogs.users.refresh_users(client)

    @commands.command(name='grab',
                description="Saves a quote.",
                pass_context=True)
    async def grab(self, context):
        try:
            msg = context.message
            onNext = False
            history = await context.message.channel.history().flatten()
            for i, message in enumerate(history):
                print(message)
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
                    description="Get a quote.",
                    pass_context=True)
    async def quote(self, context, *args):
        try:
            if (len(args) is 0):
                await context.message.channel.send(getRandQuote())
            else:
                msg = ' '.join(args)
                await context.message.channel.send(addQuote(self.members,msg))

        except Exception as e:
            print(e)
    
    @commands.command(name='lookup',
                description="Saves a quote.",
                pass_context=True)
    async def lookup(self, context, args):
        try:
            if (len(args) is None):
                await context.message.channel.send('Specify a user to lookup a quote for.')
            else:
                await context.message.channel.send(getRandQuoteOfUsers(self.members,args))
        except Exception as e:
            await context.message.channel.send('Something went wrong')
            print(e)

    '''
    @commands.command(name='deletequotes',
                    description="delete all quotes.",
                    pass_context=True)
    async def deletequotes(self, context, *args):
        try:
            conn = sqlite3.connect('quotes.db')
            c = conn.cursor()
            c.execute("Delete From quotes")
            conn.commit
            conn.close()
            await context.message.channel.send('Deleted')

        except Exception as e:
            print(e)
    '''

def addQuote(members, args):
    user = args.split()[0].strip()
    if "@" not in user:
        return "Quote could not be added, please include a user"
    print(user)
    print(members)
    if user not in members:
        return "That is not currently a member of this or any server I know."
    conn = sqlite3.connect('quotes.db')
    message = '"' + ' '.join(args.split()[1:]) + '"'
    q = (user,message)
    c = conn.cursor()
    c.execute("INSERT INTO quotes VALUES (?,?)", q)
    conn.commit()
    conn.close()
    return 'Quote added.'


def getRandQuote():
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute("SELECT * From quotes")
    result = c.fetchall()
    result = result[random.randint(0, len(result) - 1)]
    result = ' '.join(result)
    conn.close()
    return(result)


def getRandQuoteOfUsers(members, args):
    if "@" not in args:
        return('That isnt a user!')
    if args not in members:
        return "That is not currently a member of this or any server I know."

    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute("SELECT * From quotes WHERE user = (?)", (args,))
    result = c.fetchall()
    result = result[random.randint(0, len(result) - 1)]
    result = ' '.join(result)
    conn.close()
    return(result)

def set_users(users):
    pass

def setup(client):
    client.add_cog(Quote(client))

