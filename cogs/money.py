import random, re, discord, sqlite3, cogs.users
from discord.ext import commands

# table: money
# Columns: type, quantity

class Money(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='deposit',
                description='Add money to the group bank.',
                pass_context=True)
    async def deposit(self, context, *args):
        if(check_for_cash(args)):
            try:
                await context.message.channel.send(cash(args))
            except Exception as e:
                await context.message.channel.send('Money could not be added for some reason...')
                print(e)
        else:
            try:
                await context.message.channel.send(cash(args))
            except Exception as e:
                await context.message.channel.send('Money could not be added for some reason...')
                print(e)

    @commands.command(name='spend',
                description='Reduce item to the group bank.',
                pass_context=True)
    async def widthdraw(self, context, *args):
        try:
            await context.message.channel.send(reduce_balance(args))
        except Exception as e:
            await context.message.channel.send('Money could not be reduced for some reason...')
            print(e)

    @commands.command(name='cash',
                description='List all cash in bank.',
                pass_context=True)
    async def list_cash(self, context):
        try:
            await context.message.channel.send(get_balance())
        except Exception as e:
            await context.message.channel.send('Balance could not be retrieved.')
            print(e)

def check_if_string(args):
    try:
        int(args[-1])
        return True
    except Exception:
        return False

def cash(args):
    if(check_for_cash(args)):
        return update_balance(args)
    else:
        return insert_balance(args)

def reduce_balance(args):
    dec = check_if_string(args)
    if(dec):
        try:
            cash = ' '.join(args[:-1])
            cash = cash.lower()
            quantity =  int(args[-1])
            conn = sqlite3.connect('rudd.db')
            c = conn.cursor()
            c.execute('UPDATE money SET quantity = quantity - ? WHERE type = ?', (quantity,cash,))
            conn.commit()
            conn.close()
            return 'Item reduced.'
        except Exception as e:
            print(e)
    else:
        try:
            cash = ' '.join(args)
            cash.lower()
            conn = sqlite3.connect('rudd.db')
            c = conn.cursor()
            c.execute('UPDATE money SET quantity = quantity - ? WHERE type = ?', (1,cash,))
            conn.commit()
            conn.close()
            return 'Item reduced.'
        except Exception as e:
            print(e)

def update_balance(args):
    inc = check_if_string(args)
    if(inc):
        try:
            cash = ' '.join(args[:-1])
            cash = cash.lower()
            quantity =  int(args[-1])
            conn = sqlite3.connect('rudd.db')
            c = conn.cursor()
            c.execute('UPDATE money SET quantity = quantity + ? WHERE item = ?', (quantity,cash,))
            conn.commit()
            conn.close()
            return 'Balance updated.'
        except Exception as e:
            print(e)
    else:
        try:
            cash = ' '.join(args)
            cash = cash.lower()
            conn = sqlite3.connect('rudd.db')
            c = conn.cursor()
            c.execute('UPDATE money SET quantity = quantity + ? WHERE type = ?', (1,cash,))
            conn.commit()
            conn.close()
            return 'Balance updated.'
        except Exception as e:
            print(e)

def insert_balance(args):
    inc = check_if_string(args)
    if(inc):
        try:
            cash = ' '.join(args[:-1])
            cash = cash.lower()
            quantity =  int(args[-1])
            conn = sqlite3.connect('rudd.db')
            c = conn.cursor()
            c.execute('INSERT INTO money VALUES (?,?)',(cash,quantity,))
            conn.commit()
            conn.close()
            return 'Cash added'
        except Exception as e:
            print(e)
    else:
        try:
            cash = ' '.join(args)
            cash = cash.lower()
            conn = sqlite3.connect('rudd.db')
            c = conn.cursor()
            c.execute('INSERT INTO money VALUES (?,?)',(cash,1,))
            conn.commit()
            conn.close()
            return 'Cash added'
        except Exception as e:
            print(e)

def check_for_cash(args):
    try:
        cash = ' '.join(args[:-1])
        cash = cash.lower()
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT * FROM money WHERE type = ?',(cash,))
        result = c.fetchone()
        conn.close()
        if result is None:
            return False
        else:
            return True
    except Exception as e:
        print(e)

def get_balance():
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM money')
    result = c.fetchall()
    conn.close()
    result_string = 'Balance in Party Bank:\n'
    for item in result:
        result_string += str(item[0]) +', Quantity: ' + str(item[1]) +'\n'
    return result_string

def setup(client):
    client.add_cog(Money(client))

