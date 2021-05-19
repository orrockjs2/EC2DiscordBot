# bot.py
import os
import random
import start_stop_ec2

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
        'Jordan', 'Scotty', 'Mason', 'Laith', 'Alec', 'Gabe', 'Afkeo', 'Connnor',
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
        response2 = start_stop_ec2.main('shutdown')
        await message.channel.send(response2)
    if message.content.lower() == 'epiccraft' or message.content.lower() == 'startup':
        response = random.choice(startup_messages)
        await message.channel.send(response)
        response2 = start_stop_ec2.main('startup')
        commands = ['echo "hello world"', './minecraftStarter.sh']  # the echo is just for testing really
        start_stop_ec2.bash_script_executor(commands)
        await message.channel.send(response2)
        public_ip = start_stop_ec2.fetch_public_ip()
        await message.channel.send('Use this IP to login to the server: ' + str(public_ip))
    if message.content.lower() == 'addy':
        public_ip = start_stop_ec2.fetch_public_ip()
        await message.channel.send('Use this IP to login to the server: ' + str(public_ip))
    if message.content.lower() == 'help':
        response = 'Commands list: \n' \
                   'startup/epiccraft starts the EC2 server and lists the IP \n' \
                   'shutdown/cringecraft stops the EC2 server' \
                   'addy lists the current IP'
        await message.channel.send(response)

client.run(TOKEN)
