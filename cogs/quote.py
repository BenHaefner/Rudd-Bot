import random, re, discord, sqlite3
from discord.ext import commands

# TODO Convert to working with database

# Database = quotes.db
# Table = quotes
# User column: user
# Quote column: quote


class Quote(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='grab',
                description="Saves a quote.",
                pass_context=True)
    async def grab(self, context, *args):
        try:
            msg = ' '.join(args)
            #with open("quotes.txt", 'a') as myfile:
                #myfile.write(msg)
            await context.message.channel.send(addQuote(msg))
        except Exception as e:
            await context.message.channel.send('Quote could not be saved')
            print(e)


    @commands.command(name='quote',
                    description="Get a quote.",
                    pass_context=True)
    async def quote(self, context, *args):
        try:
            #if (len(args) is None):
            #    with open("quotes.txt", 'r') as myfile:
            #        msgArray = []
            #        for line in myfile:
            #            msgArray.append(line)
            #        msg = msgArray[random.randint(0, len(msgArray)-1)]
            #        await context.message.channel.send(msg)
            #else:
            #    pass
            #    # TODO Quote a person
            await context.message.channel.send(getRandQuote())

        except Exception as e:
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
    
def addQuote(args):
    conn = sqlite3.connect('quotes.db')
    user = args.split()[0].strip()
    if "@" not in user:
        return "Quote could not be added, please include a user"
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


def setup(client):
    client.add_cog(Quote(client))

