import random, re, discord, sqlite3, cogs.users
from discord.ext import commands

# table: task
# Columns: name, description


class Task(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='add_task',
                description="Saves a quote.",
                pass_context=True)
    async def add_task(self, context, *args):
        try:
            await context.message.channel.send(addTask(args))
        except Exception as e:
            await context.message.channel.send('Task could not be saved.')
            print(e)

    
    @commands.command(name='lookup_task',
                description="Saves a quote.",
                pass_context=True)
    async def lookup_task(self, context, args):
        try:
            await context.message.channel.send(lookupTask(args))
        except Exception as e:
            await context.message.channel.send('Task could not be retrieved.')
            print(e)

    @commands.command(name='list_tasks',
                description="Saves a quote.",
                pass_context=True)
    async def list_tasks(self, context):
        try:
            tasks = lookupTasks()   
            for task in tasks:
                await context.message.channel.send(task)
        except Exception as e:
            await context.message.channel.send('Task could not be retrieved.')
            print(e)

    @commands.command(name='end_task',
                description="Saves a quote.",
                pass_context=True)
    async def end_task(self, context, args):
        try:
            await context.message.channel.send(endTask(args))
        except Exception as e:
            await context.message.channel.send('Task could not be deleted.')
            print(e)

def lookupTasks():
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute("SELECT name FROM task")
        result = c.fetchall()
        conn.close()
        tasks = []
        for names in result:
            tasks.append(names[0])
        return tasks
    except Exception as e:
        print(e)

def lookupTask(args):
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute("SELECT description FROM task WHERE name = (?)", (args,))
        result = c.fetchall()
        conn.close()
        return result[0][0]
    except Exception as e:
        print(e)

def addTask(args):
    try:
        name = args[0]
        desc =  ' '.join(args[1:])
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute("INSERT INTO task VALUES (?,?)", (name,desc,))
        conn.commit()
        conn.close()
        return 'Quote added.'
    except Exception as e:
        print(e)

def endTask(args):
    try:
        conn = sqlite3.connect('rudd.db')
        c = conn.cursor()
        c.execute("DELETE FROM task WHERE name = (?)", (args,))
        conn.commit()
        conn.close()
        return "Task ended"
    except Exception as e:
        print(e)




def setup(client):
    client.add_cog(Task(client))

