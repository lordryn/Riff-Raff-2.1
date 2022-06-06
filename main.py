from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import logging
import sqlite3
import os
import discord
import pytz as pytz
from dotenv import load_dotenv
import random
import datetime
import asyncio
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# # grabs discord bot token from .env file and initializes
# load_dotenv()
my_secret = os.environ['DISCORD_TOKEN']
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!')

#         #item = command_removed.replace(' ', '_')
def check(m):
    if m.reference is not None and not m.is_system :
         return True
    return False

@bot.event
# info items done after successful bot startup/reboot
async def on_ready():
    logger.info(
        f'{bot.user} has connected to Discord!')  # discord connection verified
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="the misfits and influencing elections on Facebook"))

    # time retrieval loop
    while True:
        cst = pytz.timezone('US/Central')
        now = datetime.datetime.now(cst)
        an_chan = bot.get_channel(947328202483830794)
        refresh_time = 60  # time refresh rate in seconds

        # daily and weekly announcements

        if now.hour == 19 and now.minute == 00:
            announcement = 'A daily reset has occurrered!\n Don\'t forget You\'re daily challenges and free keys today!'
            logging.info(announcement)
            if now.weekday() == 1:
                announcement = 'A weekly reset has occurred!'
            await an_chan.send(announcement)
            if now.weekday() == 3:
                announcement = '''Weekly cit build tick!\n
                      Don't forget to help cap the resources for the cit raffle!\n
                      Don't forget to use your clan cape xp!\n
                      Don't forget to collect your xp from the quartermaster after capping!\n
                      '''
            refresh_time = 120
        await asyncio.sleep(refresh_time)


@bot.event
async def on_raw_reaction_add(payload):
    rules_message_id = 976923160387682358

    if rules_message_id == payload.message_id:
        logger.info(f"new member->{payload.member}")
        member = payload.member
        guild = member.guild
        logger.info(member.name)
        # emoji = payload.emoji.name
        # if emoji == '👍':
        role = discord.utils.get(guild.roles, name='Member')
        await member.add_roles(role)
        member_id = member.id
        member_name = member.name
        dir_name = f'Members/{member_id}({member_name})'
        if not os.path.exists(f'{dir_name}/main.db'):
            os.makedirs(dir_name)
            conn = sqlite3.connect(f'{dir_name}/main.db')


@bot.event
async def on_member_remove(member):
    text_file = open("leave.txt", "r")
    leave_list = text_file.readlines()
    text_file.close()
    channel = bot.get_channel(976928345897963600)
    list_length = len(leave_list) + 1
    logger.info(f"{member.nick}->left")
    await channel.send(
        f"{member.nick} {leave_list[random.randint(0, list_length)]}")
    
@bot.event
async def on_message_delete(message):
    logger.info(f'message: {message.content} by {message.author} was deleted in {message.channel}')

@bot.event
async def on_command(ctx):
    server = ctx.guild.name
    user = ctx.author
    command = ctx.command
    logger.info(f'{server} > {user} > {command}')
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("**Invalid command. Try using** `help` **to figure out commands!**")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**Please pass in all requirements.**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**You dont have all the requirements or permissions for using this command :angry:**")

        


@bot.command()
async def halp(ctx):
    cmds = """Riff Raff Raffler by Lord Ryn \n
        Designed for the Misfit Marauders Discord\n
        !help - this menu(list of commands)\n
        !rswiki <search query> - searches the rswiki and reports back\n
        !calc <skill> <level target> - shows how many things it'll take to level a skill
            Currently uses discord nicks for rsn. Item type selection planned in the future\n
        !raffle - chooses a user that reacts to a post
            you mus be replying to the post for the bot to get the target
            !raffle cit <days> - checks for images in the last <days> days
                The current target is the 🏰citadel-raffle channel.\n
        !rand or !random - chooses a random number 1-100\n
        !poll - currently adds a thumbs up and down to post\n
        !bonghit - make mama high again!\n
        !pushups - get ripped
        """
    await ctx.send(cmds)


@bot.command()
async def bonghit(ctx):
    username = ctx.author
    ma_id = '<@542436163395387407>'
    emoji = bot.get_emoji(977020269682106419)
    await ctx.message.add_reaction(emoji)
    await ctx.send(f'{ma_id} {username} has redeemed a bong hit!')
    logger.info(f'{username}->bonghit ')


@bot.command()
async def raffle(ctx):
    # sqlite database connect
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

    # info logging.info
    logger.info(contestants)
    logger.info(result)


@bot.command()
async def pushups(ctx):
    username = ctx.author
    bird_id = '<@240996018181636098>'
    dan_id = '<@936869866995068998>'
    massey_id = '<@111978295750303744>'
    emoji = bot.get_emoji(962177233634594826)
    await ctx.message.add_reaction(emoji)
    await ctx.send(
        f'{bird_id}, {massey_id}, and {dan_id}, {username} has redeemed 5 Push Ups!'
    )
    logger.info(f'{username}->pushups ')


@bot.command()
async def rswiki(ctx):
    await ctx.send("This command isn't currently enabled")


@bot.command()
async def calc(ctx):
    await ctx.send("This command isn't currently enabled")


@bot.command()
async def rand(ctx):
    
    await ctx.send("This command isn't currently enabled")


@bot.command()
async def poll(ctx):
    await ctx.send("This command isn't currently enabled")
@bot.command()
async def contestants(ctx):
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


@bot.command()
async def clear(ctx, amount):
    await ctx.message.delete()
    logger.info(f"{ctx.author}>clear>{amount}>{ctx.channel}")
    await ctx.message.channel.purge(limit=int(amount))
    
@bot.command(description="Echos, developers only", pass_context=True)
async def echo(ctx, echowords:str):
    message = ctx.message
    if ctx.message.author.id in [275139099415937024, 936869866995068998]: #put in id's in a list or replace it with one string\
        
        await ctx.send(echowords)
        if check(message):
            print('true')
        
    else:
        await ctx.send("Bot developers only :<")
    await message.delete()

bot.run(my_secret)
