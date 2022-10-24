import time
import os
import discord
import pytz as pytz
from dotenv import load_dotenv
import random
import datetime
import asyncio
from discord.ext import commands
from logger import Logger
from flask import Flask
from threading import Thread
import sqlite3

Logger = Logger()

# # grabs discord bot token from .env file and initializes
# load_dotenv()
my_secret = os.environ['DISCORD_TOKEN']
# client = discord.Client(intents=intents)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
cog_files = ['commands.raffle', 'commands.community', 'commands.runescape']

for cog_file in cog_files:
    bot.load_extension(cog_file)
    print("%s has loaded." % cog_file)


#         #item = command_removed.replace(' ', '_')
def check(m):
    if m.reference is not None and not m.is_system:
        return True
    return False


@bot.event
# info items done after successful bot startup/reboot
async def on_ready():
    Logger.log(
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
        days_until_holloween = 31 - int(now.day) 
        # daily and weekly announcements
            
        if now.hour == 19 and now.minute == 00:
            announcement = 'A daily reset has occurred!\n Don\'t forget your daily challenges and free keys today!'
            Logger.log(announcement)
            await an_chan.send(f"There are {days_until_holloween} days until Holloween!")
            if now.weekday() == 1:
                announcement = 'A weekly reset has occurred!'
            
            if now.weekday() == 5:
                announcement = '''Weekly cit build tick! @everyone\n
                      Don't forget to use your clan cape xp!\n
                      Don't forget to collect your xp from the quartermaster after capping!\n
                      '''
            await an_chan.send(announcement)
            refresh_time = 120
        await asyncio.sleep(refresh_time)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Misfit Marauders! If you have any problems or suggestions just message me and choose the related option.'
    )
@bot.event
async def on_raw_reaction_add(payload):
    chan = bot.get_channel(payload.channel_id)
    user = bot.get_user(payload.user_id)
    if user != bot.user:

        if isinstance(chan, discord.channel.DMChannel):
            msg_id = payload.message_id
            message = await chan.fetch_message(msg_id)
            reaction = payload.emoji
            target_id = message.reference.message_id
            original = await chan.fetch_message(id=target_id)
            msg_cont = original.content
            report_chan = bot.get_channel(994722689849757817)
            suggestion_chan = bot.get_channel(994722622250176573)

            if str(reaction) == "1️⃣":
                with open('reports.txt', 'a') as f:
                    f.write(f'{msg_cont}\n')
                await chan.send('Report submitted')
                await chan.send(f"'{msg_cont}'")
                await report_chan.send(f"'{msg_cont}'")
            if str(reaction) == "2️⃣":
                with open('suggestions.txt', 'a') as f:
                    f.write(f'{msg_cont}\n')
                await chan.send('Suggestion submitted')
                await chan.send(f"'{msg_cont}'")
                await suggestion_chan.send(f"'{msg_cont}'")
            if str(reaction) == '❌':
                pass

    try:
        rules_message_id = 976923160387682358
        if rules_message_id == payload.message_id:
            Logger.log(f"new member->{payload.member}")
            member = payload.member
            guild = member.guild
            Logger.log(member.name)
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
        # if not message.guild:
    except:
        pass


#graveyard - when a player leaves
@bot.event
async def on_member_remove(member):
    text_file = open("leave.txt", "r")
    leave_list = text_file.readlines()
    text_file.close()

    channel = bot.get_channel(976928345897963600)
    list_length = len(leave_list) + 1
    Logger.log(f"{member.nick}->left")
    await channel.send(
        f"<@{member.id}> ({member.name}/{member.nick}) {leave_list[random.randint(0, list_length)]}")


@bot.event
async def on_message_delete(message):
    Logger.log(
        f'message: {message.content} by {message.author} was deleted in {message.channel}'
    )


@bot.event
async def on_command(ctx):
    server = ctx.guild.name
    user = ctx.author
    command = ctx.command
    Logger.log(f'{server} > {user} > {command}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "**Invalid command. Try using** `help` **to figure out commands!**"
        )
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**Please pass in all requirements.**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "**You dont have all the requirements or permissions for using this command :angry:**"
        )


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
async def rand(ctx):

    await ctx.send("This command isn't currently enabled")


@bot.command()
async def clear(ctx, amount):
    await ctx.message.delete()
    Logger.log(f"{ctx.author}>clear>{amount}>{ctx.channel}")
    await ctx.message.channel.purge(limit=int(amount))


@bot.command(description="Echos, developers only", pass_context=True)
async def echo(ctx, echowords: str):
    message = ctx.message
    if ctx.message.author.id in [
            275139099415937024, 936869866995068998
    ]:  #put in id's in a list or replace it with one string\

        await ctx.send(echowords)
        if check(message):
            print('true')

    else:
        await ctx.send("Bot developers only :<")
    await message.delete()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not message.guild and message.author != bot.user:
        try:
            Logger.log(f'{message.author} {message.content}')
            confirmation = await message.reply("""Is this a 
                :one: report 
                or 
                :two: suggestion
            
            Both are anonymous
            With reports please give the following:
                -user's name(in game or discord both work)
                -aproximate time of event
                -a summary of the event.
            If you need to cancel or change information click/tap the :x:
            and then send a new message
                
                """)
            reactions = ['1️⃣', '2️⃣', '❌']
            for reaction in reactions:
                await confirmation.add_reaction(reaction)
        except discord.errors.Forbidden:
            Logger.log("fail")
            pass
    else:
        pass
    await bot.process_commands(message)


try:
    bot.run(my_secret)
except:
    quit
