import os
import random
import start_stop_ec2
import time
from mcstatus import MinecraftServer
from pprint import pprint
import subprocess

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event  # for when bot connects to server for the first time
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for server in client.guilds:
        for channel in server.text_channels:
            if channel.permissions_for(server.me).send_messages:
                await channel.send('CringeCraft Bot is running')
                response = 'Commands list: \n\n' \
                           '`$startup`/`$epiccraft` starts the EC2 server and lists the IP \n' \
                           '`$shutdown`/`$cringecraft` stops the EC2 server\n' \
                           '`$addy` lists the current IP\n' \
                           '`$bounceMcServer` will restart the Minecraft server on the EC2 box\n' \
                           '`$status` will tell you if the the EC2 server is up or down (doesn\'t know if MC is up)\n' \
                           '`$howto` will give an overview of how to launch modded minecraft and set your memory\n' \
                           '`$cost` will print out current monthly cost of AWS service\n' \
                           '`$backup` will create a backup of today\'s map (can only run if server is up)\n' \
                           '`$whoup` will print out current player list'
                await channel.send(response)
                break


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    player_names = [
        'Jordan', 'Scotty', 'Mason', 'Laith', 'Alec', 'Gabe', 'Afkeo', 'Connner',
        'Daz', 'MattyElps', 'Jack', 'malikd804'
    ]

    shutdown_messages = [
        'Shutting down the server',
        'Server dead',
        random.choice(player_names) + ' needs to go to bed',
        'Jordan\'s about to get smurfed by fins',
        'Daz killed it',
        'Overwatch?'
    ]

    startup_messages = [
        'Server is starting up',
        'time to get epic',
        'Welcome to game of the week'
    ]

    how_to_message = 'Using curseforge.net [https://download.curseforge.com/], go into your settings -> game specific settings -> ' \
                     'minecraft. Under the Java settings, slide the memory slider all the way to the right (max it out). Then find Jordan\'s ' \
                     'modpack. You should be able to launch the game from curseforge with all the mods included in Jordan\'s pack'

    if message.content.lower() == '$cringecraft' or message.content.lower() == '$shutdown':
        response = random.choice(shutdown_messages)
        await message.channel.send(response)
        response2 = start_stop_ec2.main('shutdown')  # TODO: format this json into something useful
        # await message.channel.send(response2)  # this plain text prints the instance id among other things

    if message.content.lower() == '$epiccraft' or message.content.lower() == '$startup':
        response = random.choice(startup_messages)
        await message.channel.send(response)
        response2 = start_stop_ec2.main('startup')  # TODO: format this json into something useful
        # commands = ['sh /home/ubuntu/minecraftStarter.sh'] -- using rc.local for now
        # need to figure out a way to make sure server is up before doing this, for now, sleep(60)
        # time.sleep(60)
        # start_stop_ec2.bash_script_executor(commands)
        # await message.channel.send(response2) # this plain text prints instance id among other things
        await message.channel.send('grabbing the IP... will take a minute')
        time.sleep(60)
        public_ip = start_stop_ec2.fetch_public_ip()
        await message.channel.send(
            'It may take about 5 minutes to get the minecraft server up (you\'ll see a connection refused error if its not ready) ' +
            ', wait a bit and then use this IP to login to the server: `' + str(public_ip) + ':25565`')

    if message.content.lower() == '$addy':
        await message.channel.send('One sec...')
        public_ip = start_stop_ec2.fetch_public_ip()
        await message.channel.send('Use this IP to login to the server: `' + str(public_ip) + ":25565`")

    if message.content.lower() == '$bouncemcserver':
        response = 'restarting Minecraft Server'
        print('bouncing server')
        await message.channel.send(response)
        commands = ['sh /opt/scripts/minecraft.sh']
        start_stop_ec2.bash_script_executor(commands)

    if message.content.lower() == '$status':
        response = start_stop_ec2.current_status()
        print(response)
        print()
        await message.channel.send(response)

    if message.content.lower() == '$howto':
        await message.channel.send(how_to_message)

    if message.content.lower() == '$aleksstatusinthediscord':
        await message.channel.send('most certainly unepic. In fact quite cringe.')

    if message.content.lower() == '$overwatch':
        await message.channel.send('officially the only move in the discord.')

    if message.content.lower() == '$cost':
        # Get current price for a given instance, region and os
        price = start_stop_ec2.get_price()
        await message.channel.send(price)

    if message.content.lower() == '$whoup':
        await message.channel.send('one sec...')
        address = str(start_stop_ec2.fetch_public_ip())
        server = MinecraftServer.lookup(str(address) + ":25565")
        try:
            query = server.query()
            if address is not None:
                if query.players.online > 0:
                    await message.channel.send("These players are online: {0}".format(", ".join(query.players.names)))
                else:
                    await message.channel.send('no one is online :(')
            else:
                await message.channel.send('server is either down or hasn\'t started.')
        except Exception:
            await message.channel.send('server is either down or hasn\'t started.')

    if message.content.lower() == '$whocringe':
        response = random.choice(player_names)
        await message.channel.send(response)

    if message.content.lower() == '$whoepic':
        response = random.choice(player_names)
        await message.channel.send(response)

    if message.content.lower() == '$help':
        response = 'Commands list: \n\n' \
                   '`$startup`/`$epiccraft` starts the EC2 server and lists the IP \n' \
                   '`$shutdown`/`$cringecraft` stops the EC2 server\n' \
                   '`$addy` lists the current IP\n' \
                   '`$bounceMcServer` will restart the Minecraft server on the EC2 box\n' \
                   '`$status` will tell you if the the EC2 server is up or down (doesn\'t know if MC is up) \n' \
                   '`$howto` will give an overview of how to launch modded minecraft and set your memory\n' \
                   '`$cost` will print out current monthly cost of AWS service\n' \
                   '`$backup` will create a backup of today\'s map (can only run if server is up)\n' \
                   '`$whoup` will print out current player list'
        await message.channel.send(response)

    if message.content.lower() == '$backup':
        start = 'Starting backup of todays map'
        response = 'Created backup of todays map'
        error = 'Something went wrong, backup not created'
        public_ip = start_stop_ec2.fetch_public_ip()
        # subprocess.call("./scripts/mcBackupBotCall.sh", shell=True)
        await message.channel.send(start)
        try:
            subprocess.check_call("./scripts/mcBackupBotCall.sh '%s'" % public_ip, shell=True)
            await message.channel.send(response)
            #TODO: add a call to delete the tar on the ec2 box here
        except:
            await message.channel.send(error)



client.run(TOKEN)
