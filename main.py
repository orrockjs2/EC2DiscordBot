import os
import random
import start_stop_ec2
import time


import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    player_names = [
        'Jordan', 'Scotty', 'Mason', 'Laith', 'Alec', 'Gabe', 'Afkeo', 'Connner',
        'Jacob', 'CringeKeating', 'MattyElps', 'Jack', 'malikd804'
    ]

    shutdown_messages = [
        'Shutting down the server',
        'Server dead',
        random.choice(player_names) + ' needs to go to bed',
        'Guess its time for game of the week',
        'Jordan\'s about to get smurfed by fins'
    ]

    startup_messages = [
        'Server is starting up',
        'time to get epic',
        'Welcome to game of the week'
    ]

    if message.content.lower() == 'cringecraft' or message.content.lower() == 'shutdown':
        response = random.choice(shutdown_messages)
        await message.channel.send(response)
        response2 = start_stop_ec2.main('shutdown')  # TODO: format this json into something useful
        # await message.channel.send(response2)  # this plain text prints the instance id among other things

    if message.content.lower() == 'epiccraft' or message.content.lower() == 'startup':
        response = random.choice(startup_messages)
        await message.channel.send(response)
        response2 = start_stop_ec2.main('startup')  # TODO: format this json into something useful
        commands = ['sh /home/ubuntu/minecraftStarter.sh']
        # need to figure out a way to make sure server is up before doing this, for now, sleep(60)
        time.sleep(60)
        start_stop_ec2.bash_script_executor(commands)
        # await message.channel.send(response2) # this plain text prints instance id among other things
        await message.channel.send('grabbing the IP...')
        public_ip = start_stop_ec2.fetch_public_ip()
        await message.channel.send('Use this IP to login to the server: ' + str(public_ip) + ':25565')

    if message.content.lower() == 'addy':
        await message.channel.send('One sec...')
        public_ip = start_stop_ec2.fetch_public_ip()
        await message.channel.send('Use this IP to login to the server: ' + str(public_ip))

    if message.content.lower() == 'bouncemcserver':
        response = 'restarting Minecraft Server'
        print('bouncing server')
        await message.channel.send(response)
        commands = ['sh /home/ubuntu/minecraftStarter.sh']
        start_stop_ec2.bash_script_executor(commands)

    if message.content.lower() == 'status':
        response = start_stop_ec2.current_status()
        print(response)
        print()
        await message.channel.send(response)

    if message.content.lower() == 'help':
        response = 'Commands list: \n\n' \
                   '`startup`/`epiccraft` starts the EC2 server and lists the IP \n' \
                   '`shutdown`/`cringecraft` stops the EC2 server\n' \
                   '`addy` lists the current IP\n'\
                   '`bounceMcServer` will start the Minecraft server on the EC2 box\n'\
                   '`status` will tell you if the the EC2 server is up or down'
        await message.channel.send(response)

client.run(TOKEN)
