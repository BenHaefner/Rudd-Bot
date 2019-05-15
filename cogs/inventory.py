import random, re, discord, sqlite3, cogs.users
from discord.ext import commands

# table: inventory/money
# Columns: item, quanitity/type, quantity

class Inventory(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='add_item',
                description='Add item to the group inventory.',
                pass_context=True)
    async def add_item(self, context, *args):
        try:
            await context.message.channel.send(item(args))
        except Exception as e:
            await context.message.channel.send('Item could not be added for some reason...')
            print(e)

    @commands.command(name='use_item',
                description='Reduce item to the group inventory.',
                pass_context=True)
    async def use_item(self, context, *args):
        try:
            await context.message.channel.send(reduce_item(args))
        except Exception as e:
            await context.message.channel.send('Item could not be reduced for some reason...')
            print(e)

    @commands.command(name='items',
                description='List all items in inventory.',
                pass_context=True)
    async def get_items(self, context):
        try:
            await context.message.channel.send(get_item_list())
        except Exception as e:
            await context.message.channel.send('Items could not be retrieved.')
            print(e)

    @commands.command(name='clean_items',
                description='Remove all items from inventory with Quantity Zero.',
                pass_context=True)
    async def clean_items(self, context):
        try:
            await context.message.channel.send(cleanup())
        except Exception as e:
            await context.message.channel.send('Items could not be cleaned.')
            print(e)

def item(args):
    if(check_for_item(args)):
        return update_item(args)
    else:
        return insert_item(args)

def reduce_item(args):
    try:
        item = ' '.join(args[:-1])
        quantity =  int(args[-1])
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('UPDATE inventory SET quantity = quantity - ? WHERE item = ?', (quantity,item,))
        conn.commit()
        conn.close()
        return 'Item reduced.'
    except Exception as e:
        print(e)

def update_item(args):
    try:
        item = ' '.join(args[:-1])
        quantity =  int(args[-1])
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('UPDATE inventory SET quantity = quantity + ? WHERE item = ?', (quantity,item,))
        conn.commit()
        conn.close()
        return 'Item updated.'
    except Exception as e:
        print(e)

def insert_item(args):
    try:
        item = ' '.join(args[:-1])
        print(args[-1])
        quantity =  int(args[-1])
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('INSERT INTO inventory VALUES (?,?)',(item,quantity,))
        conn.commit()
        conn.close()
        return 'Item added'
    except Exception as e:
        print(e)

def check_for_item(args):
    try:
        item = ' '.join(args[:-1])
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('SELECT * FROM inventory WHERE item = ?',(item,))
        result = c.fetchone()
        conn.close()
        if result is None:
            return False
        else:
            return True
    except Exception as e:
        print(e)

def get_item_list():
    conn = sqlite3.connect('rudd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    result = c.fetchall()
    conn.close()
    result_string = 'Items in Party Inventory:\n'
    for item in result:
        result_string += str(item[0]) +', Quantity: ' + str(item[1]) +'\n'
    return result_string

def cleanup():
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('DELETE FROM inventory WHERE quantity <= 0')
        conn.commit()
        conn.close()
        return 'Items cleaned'
    except Exception as e:
        print(e)

def setup(client):
    client.add_cog(Inventory(client))

