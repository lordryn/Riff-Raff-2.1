import sqlite3
import discord
from discord.ext import commands
from logger import Logger
Logger = Logger()


class Raffler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def raffle(self, ctx): 
        conn = sqlite3.connect('raffle.sqlite')
        cur = conn.cursor()
    
        # clears name table for fresh raffle
        cur.executescript(
            '\n'
            '			DROP TABLE IF EXISTS Name;\n'
            '			CREATE TABLE Name (\n'
            '				id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n'
            '				name   TEXT\n'
            '			);\n'
            '			')
    
        # Discord message scrape
        msg_id = ctx.message.reference.message_id
        chan = ctx.channel
        msg = await chan.fetch_message(msg_id)
    
        # creates set and grabs reacted users
        users = set()
        for reaction in msg.reactions:
            async for user in reaction.users():
                users.add(user.id)
    
        # takes the userdata and commits the usernames to the database
        contestants = []
        for entrant in users:
            cur.execute('INSERT INTO Name (name)\n'
                        '					VALUES ( ? )', (str(entrant), ))
            cur.execute('SELECT id FROM Name WHERE name = ? ', (str(entrant), ))
            conn.commit()
            contestants.append(entrant)  # infoging list of entrants
    
        # picks a winner
        cur.execute('''SELECT name FROM Name ORDER BY RANDOM() LIMIT 1'''
                    )  # there is room to have multiple winners
        winner = cur.fetchone()[0]
    
        # results message construction and push
        number_of_contestants = len(contestants)
        result = f"Out of {number_of_contestants} contestants, <@{winner}> has won the raffle!"
        conn.close()
        await ctx.send(result)
        Logger.log(contestants)
        Logger.log(result)
        
    @commands.command()
    async def contestants(self, ctx):
        con = sqlite3.connect("raffle.sqlite")
        cursor = con.cursor()
        
        query = "SELECT name FROM Name"
        cursor.execute(query)
        a1 = cursor.fetchall()
        print(a1)
        a2 = []
        for i in a1:
            i2= str(i)
            i3 = i2.replace('(','').replace(')','').replace(',', '').replace("'", '')
            a2.append(f'<@{i3}>')
        print(a2)
        await ctx.send(f"Contestants:\n{a2}")
        con.close()
def setup(bot):
    bot.add_cog(Raffler(bot))
        # info Logger.logging.info
        #Logger.logger.info(contestants)
        #Logger.logger.info(result)