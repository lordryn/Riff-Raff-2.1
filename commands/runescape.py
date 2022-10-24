import discord
from discord.ext import commands
from logger import Logger
Logger = Logger()

class Runescape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def rswiki(self, ctx):
        await ctx.send("This command isn't currently enabled")
    
    
    @commands.command()
    async def calc(self, ctx):
        await ctx.send("This command isn't currently enabled")


    
def setup(bot):
    bot.add_cog(Runescape(bot))