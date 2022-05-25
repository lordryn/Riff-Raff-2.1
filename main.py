from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import sqlite3
import os
import discord
import pytz as pytz
from dotenv import load_dotenv
import random
import datetime
import asyncio


intents = discord.Intents.all()


# grabs discord bot token from .env file and initializes
load_dotenv()
my_secret = os.environ['DISCORD_TOKEN']
client = discord.Client(intents=intents)

        #item = command_removed.replace(' ', '_')

@client.event
# debug items done after successful bot startup/reboot
async def on_ready():
    print(f'{client.user} has connected to Discord!'
          )  # discord connection verified
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the misfits and influencing elections on Facebook"))


    # time retrieval loop
    while True:
        cst = pytz.timezone('US/Central')
        now = datetime.datetime.now(cst)
        an_chan = client.get_channel(947328202483830794)
        refresh_time = 60  # time refresh rate in seconds

        # daily and weekly announcements

        if now.hour == 19 and now.minute == 00:
            announcement = 'A daily reset has occurrered!\n Don\'t forget You\'re daily challenges and free keys today!'
            print(announcement)
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


@client.event
async def on_raw_reaction_add(payload):
    rules_message_id = 976923160387682358

    if rules_message_id == payload.message_id:
        print(f"new member->{payload.member}")
        member = payload.member
        guild = member.guild
        print(member.name)
        # emoji = payload.emoji.name
        # if emoji == '👍':
        role = discord.utils.get(guild.roles, name='Member')
        await member.add_roles(role)

@client.event
async def on_member_remove(member):
    text_file = open("leave.txt", "r")
    leave_list = text_file.readlines()
    text_file.close()
    channel = client.get_channel(976928345897963600)
    list_length = len(leave_list) + 1
    print(f"{member.nick}->left")
    await channel.send(f"{member.nick} {leave_list[random.randint(0, list_length)]}")


def first_word(mess):
    return mess.lower().split(' ')[0]
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_position(0, 0)
driver.set_window_size(1000, 2000)

@client.event
# constantly monitors all channels the bot has access to and responds to keywords accordingly
async def on_message(message):
    username = str(message.author).split('#')[
        0]  # username grab and removal of discriminator
    user_message = str(message.content)
    channel = message.channel
    com = first_word(user_message)
    
    # omits bot chats
    if message.author == client.user:
        return

    # help list of current commands, secret commands omitted
    if com == '!help':
        cmds = """Riff Raff Raffler by Lord Ryn \n
        Designed for the Misfit Marauders Discord\n
        !help - this menu(list of commands)\n
        !raffle - chooses a user that reacts to a post*\n
        !list - lists all users who react to a post*\n
        !rand or !random - chooses a random number 1-100\n
        !poll - currently adds a thumbs up and down to post\n
        !rswiki - creates a link based on post command text\n
        *list and raffle require you to be replying to the target post\n
        *raffle currently only works in a channel named 🎫weekly-raffle
        """
        await message.channel.send(cmds)

    # reacts to positive affirmation
    if user_message.lower() == 'good bot':
        print(f'{username}->{user_message}')
        await message.channel.send('💖')
    # todo add db access to tally affirmations

    # negative reaction to mark poor experience
    if user_message.lower() == 'bad bot':
        print(f'{username}->{user_message}')
        await message.channel.send('😔')

    # todo add suggestions command
    #ma's bonghits
    if com == '!bonghit':
        ma_id = '<@542436163395387407>'
        emoji = client.get_emoji(977020269682106419)
        await message.add_reaction(emoji)
        await message.channel.send(f'{ma_id} {username} has redeemed a bong hit!')
        print(f'{username}->bonghit ')
    if com == '!pushups':
        bird_id = '<@240996018181636098>'
        dan_id = '<@936869866995068998>'
        massey_id = '<@111978295750303744>∆'
        emoji = client.get_emoji(962177233634594826)
        await message.add_reaction(emoji)
        await message.channel.send(f'{bird_id}, {massey_id}, and {dan_id}, {username} has redeemed 5 Push Ups!')
        print(f'{username}->pushups ')
        

    # converts post command text to rswiki link
    if com == '!rswiki':
        command_removed = user_message.lower().replace('!rswiki ', '')
        item = command_removed.replace(' ', '_')

        driver.get("https://runescape.wiki/")
        time.sleep(1)

        input_box = driver.find_element(By.NAME, "search")

        input_box.send_keys(command_removed)
        
        input_box.send_keys(Keys.ENTER)
        title = driver.find_element(By.ID, "firstHeading")
        link = driver.current_url
        print(f'{username}->{item}->{link}')
        
        if title.text != 'Search results':
            await message.channel.send(f'\n{link}')
        else:
            results = driver.find_element(By.CLASS_NAME, 'searchresults')
            results.screenshot("screenshot.png")
            await message.channel.send(f'Search results for: {item}\n {link} ', file = discord.File('screenshot.png'))
    # bot greeting for testing
    if com == '!calc':#https://runescape.wiki/w/Calculator:
        command_removed = user_message.lower().replace('!calc ', '')
        skill = first_word(command_removed)
        skill = skill.capitalize()
        skill_removed = command_removed.replace(first_word(command_removed), '')
        author_id = await client.fetch_user(message.author.id)
        rsn = message.author.nick
        print (rsn)
        target = skill_removed.split(' ')[1]
        print(target)
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_position(0, 0)
        driver.set_window_size(4000, 4000)
        driver.get(f"https://www.runehq.com/calculator/{skill}")
        time.sleep(1)

        username = driver.find_element(By.NAME, 'username')
        username.send_keys(rsn)
        time.sleep(0.5)
        goal_field = driver.find_element(By.NAME, 'goal')
        goal_field.clear()
        goal_field.send_keys(target)
        time.sleep(0.5)
        calculate_button = driver.find_element(By.XPATH, '//*[@id="calcForm"]/div[1]/div/input[4]')
        calculate_button.click()

        item_table = driver.find_element(By.ID, 'item-table')
        item_table.screenshot('screenshot.png')
        
        await message.channel.send(f'GL\n{driver.current_url}', file = discord.File('screenshot.png'))
        
    if user_message.lower() == 'hello riff raff':
        print(f'{username}->{user_message}')
        await message.channel.send(f'Hello {username}')

    # generates a random number
    elif com == '!random' or com == '!rand':
        print(com)
        try:
            randrange = int(user_message.lower().split(' ')[1])
        except IndexError:
            randrange = 100
        random_number = random.randrange(randrange)
        print(f'{username}->{user_message}->{random_number}')
        response = f'From 1-{randrange} I have chosen: {random_number}'  # todo add ability to specify the range
        await message.channel.send(response)

    # polling, thumbs up or down
    if com == '!poll':
        # todo? add number to specify multiple choice
        yn_emojis = ['\N{THUMBS UP SIGN}', '\N{THUMBS DOWN SIGN}']
        print(f'{username}->{user_message}')
        for emoji in yn_emojis:
            await message.add_reaction(emoji)

    # lists users that react to a post
    if com == '!list':
        print(f'{username}->{user_message}')
        msg_id = message.reference.message_id  # targets replied message
        chan = message.channel
        msg = await chan.fetch_message(msg_id)  # grabs target id

        # adds users to a dataset
        users = set()
        for reaction in msg.reactions:
            async for user in reaction.users():
                users.add(user)

        # user's names are extracted and posted
        await message.channel.send(
            f"users: {', '.join(user.name for user in users)}")
        print(f"users: {', '.join(user.name for user in users)}")

    # the main show, the raffle
    if True:  # channel prerequisite, more may be added using and
        
        # raffle init
        if com == '!raffle':
            print(f'{username}->{user_message}')
            if user_message.lower().split(' ')[1] == 'cit':
                print('cit raffle init')
                days_var = int(user_message.lower().split(' ')[2])
                print(days_var)
                raff_chan = client.get_channel(961795576972857354)
                message_list = await raff_chan.history().flatten()
                #print(message_list)
                                # sqlite database connect
                conn = sqlite3.connect('raffle.sqlite')
                cur = conn.cursor()
    
                # clears name table for fresh raffle
                cur.executescript('\n'
                                  '			DROP TABLE IF EXISTS Name;\n'
                                  '			CREATE TABLE Name (\n'
                                  '				id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n'
                                  '				name   TEXT\n'
                                  '			);\n'
                                  '			')
                contestants = []
                for messages in message_list:
                    #print(messages.created_at)
                    #print(datetime.datetime.utcnow().date())
                    if datetime.datetime.utcnow().date() - messages.created_at.date() <= datetime.timedelta(days=days_var):
                        
                        #print(messages.created_at.date())
                        if (messages.attachments or len(messages.embeds) != 0):
                            if messages.author.id != 936869866995068998:
                                print(messages.author.id)
                                entrant = messages.author.id
                                cur.execute(
                                    'INSERT INTO Name (name)\n'
                                    '					VALUES ( ? )', (str(entrant),))
                                cur.execute('SELECT id FROM Name WHERE name = ? ',
                                            (str(entrant),))
                                conn.commit()
                                contestants.append(entrant)  # debugging list of entrants
                
                            # picks a winner
                            cur.execute('''SELECT name FROM Name ORDER BY RANDOM() LIMIT 1'''
                                        )  # there is room to have multiple winners
                            winner = cur.fetchone()[0]
                                        # results message construction and push
                number_of_contestants = len(contestants)
                result = f"Out of {number_of_contestants} contestants, <@{winner}> has won the raffle!"
                await message.channel.send(result)
                        #DO STUFF
                
                        
                    
            else:
                # sqlite database connect
                conn = sqlite3.connect('raffle.sqlite')
                cur = conn.cursor()
    
                # clears name table for fresh raffle
                cur.executescript('\n'
                                  '			DROP TABLE IF EXISTS Name;\n'
                                  '			CREATE TABLE Name (\n'
                                  '				id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n'
                                  '				name   TEXT\n'
                                  '			);\n'
                                  '			')
    
                # Discord message scrape
                msg_id = message.reference.message_id
                chan = message.channel
                msg = await chan.fetch_message(msg_id)
    
                # creates set and grabs reacted users
                users = set()
                for reaction in msg.reactions:
                    async for user in reaction.users():
                        users.add(user.id)
    
                # takes the userdata and commits the usernames to the database
                contestants = []
                for entrant in users:
                    cur.execute(
                        'INSERT INTO Name (name)\n'
                        '					VALUES ( ? )', (str(entrant),))
                    cur.execute('SELECT id FROM Name WHERE name = ? ',
                                (str(entrant),))
                    conn.commit()
                    contestants.append(entrant)  # debugging list of entrants
    
                # picks a winner
                cur.execute('''SELECT name FROM Name ORDER BY RANDOM() LIMIT 1'''
                            )  # there is room to have multiple winners
                winner = cur.fetchone()[0]
    
                
                # results message construction and push
                number_of_contestants = len(contestants)
                result = f"Out of {number_of_contestants} contestants, <@{winner}> has won the raffle!"
                await message.channel.send(result)
    
                # debug print
                print(contestants)
                print(result)
    if com == '!clear':
        amount = int(user_message.split(' ')[1])
        await message.delete()
        await message.channel.purge(limit=amount)
    if com == '!chanid':
        await message.channel.send(channel.id)
    
    # weekly event


client.run(my_secret)
