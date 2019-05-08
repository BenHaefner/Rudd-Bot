import random, re, discord, sqlite3, cogs.users
from discord.ext import commands

# table: inventory/money
# Columns: item, quanitity/type, quantity

class Inventory(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='item',
                description='Add item to the group inventory.',
                pass_context=True)
    async def add_item(self, context, *args):
        try:
            await context.message.channel.send(item(args))
        except Exception as e:
            await context.message.channel.send('Item could not be added for some reason...')
            print(e)

def item(args):
    if(check_for_item(args)):
        update_item(args)
    else:
        insert_item(args)

def update_item(args):
    try:
        item = ' '.join(args[:-1])
        quantity =  args[:-1]
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
        quantity =  args[:-1]
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute('INSERT INTO inventory VALUES (?,?)',(item,quantity,))
        conn.commit()
        conn.close()
        return 'Item added'
    except Exception as e:
        print(e)

def check_for_item(args):
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

def setup(client):
    client.add_cog(Inventory(client))

