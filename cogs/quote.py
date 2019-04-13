import random
import discord
from discord.ext import commands


class Quote(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(name='grab',
                description="Saves a quote.",
                pass_context=True)
    async def grab(self, context):
        msg = context.message.content + "\n"
        msg = msg.replace("$grab ", "")
        try:
            with open("quotes.txt", 'a') as myfile:
                myfile.write(msg)
            await context.message.channel.send('Quote saved')
        except Exception:
            await context.message.channel.send('Quote could not be saved')


    @commands.command(name='quote',
                    description="Get a quote.",
                    pass_context=True)
    async def quote(self, context):
        try:
            with open("quotes.txt", 'r') as myfile:
                msgArray = []
                for line in myfile:
                    msgArray.append(line)
                msg = msgArray[random.randint(0, len(msgArray)-1)]
                await context.message.channel.send(msg)
        except Exception:
            print("Something went wrong")


def setup(client):
    client.add_cog(Quote(client))

