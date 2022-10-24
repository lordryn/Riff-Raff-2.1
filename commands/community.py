import discord
from discord.ext import commands
from logger import Logger
Logger = Logger()

class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def bonghit(self, ctx):
        username = ctx.author
        ma_id = '<@542436163395387407>'
        emoji = self.bot.get_emoji(977020269682106419)
        await ctx.message.add_reaction(emoji)
        await ctx.send(f'{ma_id} {username} has redeemed a bong hit!')
        Logger.log(f'{username}->bonghit ')
    
    @commands.command()
    async def pushups(self, ctx):
        username = ctx.author
        bird_id = '<@240996018181636098>'
        dan_id = '<@936869866995068998>'
        massey_id = '<@111978295750303744>'
        emoji = self.bot.get_emoji(962177233634594826)
        await ctx.message.add_reaction(emoji)
        await ctx.send(
            f'{bird_id}, {massey_id}, and {dan_id}, {username} has redeemed 5 Push Ups!'
        )
        Logger.log(f'{username}->pushups ')
    @commands.command()
    async def poll(self, ctx, options:int):
        if options == 2:
            emojis = ['\N{THUMBS UP SIGN}', '\N{THUMBS DOWN SIGN}']
           
        if  options == 3:
            emojis = ["1️⃣","2️⃣","3️⃣"]
        if  options == 4:
            emojis = ["1️⃣","2️⃣","3️⃣","4️⃣"]
        if  options == 5:
            emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
        if  options == 6:
            emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]
        if  options == 7:
            emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣"]
        if  options == 8:
            emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣"]
        if  options == 9:
            emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
        if  options == 10:
            emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        
            
        for emoji in emojis:
            await ctx.message.add_reaction(emoji)
        await ctx.message.edit(content="newcontent")

def setup(bot):
    bot.add_cog(Community(bot))