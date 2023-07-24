import os
import random
import start_stop_ec2
import time
from mcstatus import JavaServer
from pprint import pprint
import subprocess

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot()

TOKEN = os.getenv('DISCORD_TOKEN')


player_names = [
    'Jordan', 'Scotty', 'Mason', 'Laith', 'Alec', 'Gabe', 'Afkeo', 'Connner',
    'Daz', 'MattyElps', 'Jack', 'malikd804, Jacob'
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

# client = discord.Client()
# intents = discord.Intents.default()
# intents.message_content=  True


@client.event  # for when bot connects to server for the first time
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for server in client.guilds:
        for channel in server.text_channels:
            if channel.permissions_for(server.me).send_messages:
                await channel.send('CringeCraft Bot is running')
                response = 'Commands list: \n\n' \
                           '`/startup` starts the EC2 server and lists the IP \n' \
                           '`/shutdown` stops the EC2 server\n' \
                           '`/addy` lists the current IP\n' \
                           '`/bounceMcServer` will restart the Minecraft server on the EC2 box\n' \
                           '`/status` will tell you if the the EC2 server is up or down (doesn\'t know if MC is up)\n' \
                           '`/how_to` will give an overview of how to launch modded minecraft and set your memory\n' \
                           '`/cost` will print out current monthly cost of AWS service\n' \
                           '`/backup` will create a backup of today\'s map (can only run if server is up)\n' \
                           '`/who_up` will print out current player list'
                await channel.send(response)
                break


@client.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@client.slash_command(name = "startup", description = "startup the minecraft server")
async def startup(ctx):
    response = random.choice(startup_messages)
    await ctx.respond(response)
    response2 = start_stop_ec2.main('startup')  # TODO: format this json into something useful
    # commands = ['sh /home/ubuntu/minecraftStarter.sh'] -- using rc.local for now
    # need to figure out a way to make sure server is up before doing this, for now, sleep(60)
    # time.sleep(60)
    # start_stop_ec2.bash_script_executor(commands)
    # await message.channel.send(response2) # this plain text prints instance id among other things
    await ctx.respond('grabbing the IP... will take a minute')
    time.sleep(60)
    public_ip = start_stop_ec2.fetch_public_ip()
    await ctx.respond(
        'It may take about 5 minutes to get the minecraft server up (you\'ll see a connection refused error if its not ready) ' +
        ', wait a bit and then use this IP to login to the server: `' + str(public_ip) + ':25565`')


@client.slash_command(name = "shutdown", description = "shutdown the minecraft server")
async def shutdown(ctx):
    response = random.choice(shutdown_messages)
    await ctx.respond(response)
    response2 = start_stop_ec2.main('shutdown')  # TODO: format this json into something useful
    # await message.channel.send(response2)  # this plain text prints the instance id among other things


@client.slash_command(name = "addy", description = "get current IP address")
async def addy(ctx):
    await ctx.respond('One sec...')
    public_ip = start_stop_ec2.fetch_public_ip()
    await ctx.respond('Use this IP to login to the server: `' + str(public_ip) + ":25565`")


@client.slash_command(name = "bounce", description = "restart server")
async def bounce(ctx):
    response = 'restarting Minecraft Server'
    print('bouncing server')
    await ctx.respond(response)
    commands = ['sh /opt/scripts/minecraft.sh']
    start_stop_ec2.bash_script_executor(commands)


@client.slash_command(name = "status", description = "get current server status")
async def status(ctx):
    response = start_stop_ec2.current_status()
    print(response)
    print()
    await ctx.respond(response)


@client.slash_command(name = "how_to", description = "how to install modpack")
async def how_to(ctx):
    await ctx.respond(how_to_message)


@client.slash_command(name = "backup", description = "backup current server map")
async def backup(ctx):
    start = 'Starting backup of todays map'
    response = 'Created backup of todays map'
    error = 'Something went wrong, backup not created'
    await ctx.respond('grabbing IP for backup')
    public_ip = start_stop_ec2.fetch_public_ip()
    # subprocess.call("./scripts/mcBackupBotCall.sh", shell=True)
    await ctx.respond(start)
    try:
        subprocess.check_call("./scripts/mcBackupBotCall.sh '%s'" % public_ip, shell=True)
        await ctx.respond(response)
        #TODO: add a call to delete the tar on the ec2 box here
    except:
        await ctx.respond(error)

@client.slash_command(name = "cost", description = "cost of server as of yesterday")
async def cost(ctx):
    # Get current price for a given instance, region and os
    price = start_stop_ec2.get_price()
    await ctx.respond(price)


@client.slash_command(name = "who_up", description = "who is currently on the server")
async def who_up(ctx):
    await ctx.respond('one sec...')
    address = str(start_stop_ec2.fetch_public_ip())
    server = JavaServer.lookup(str(address)+":25565")

    # if ctx.author.id == 386595668199997470:
    #     await ctx.respond('Not Alec!')
    #     return

    try:
        if address is not None:
            status = server.status()
            print(f"The server has {status.players.online} players and replied in {status.latency} ms")
            if status.players.online == 0:
                await ctx.respond('no one is online :(')
                return
            else:
                players = "These players are online: "\
                          + str([user['name'] for user in status.raw['players']['sample']])\
                              .replace("'", "").replace("[", "").replace("]", "")
                await ctx.respond(players)
        else:
            await ctx.respond('server is either down or hasn\'t started.')
    except Exception as e:
        print(e)
        await ctx.respond('server is either down or hasn\'t started.')

# @client.command()
# async def test(ctx):
#     await ctx.send('test')
#
# @client.event
# async def on_message(message):
#     username = str(message.author).split("#")[0]
#     channel = str(message.channel.name)
#     user_message = str(message.content)
#     print(f'Message {user_message} by {username} on {channel}')
#     if message.author == client.user:
#         return

#

#

#
#
#     if message.content.lower() == '$aleksstatusinthediscord':
#         await message.channel.send('most certainly unepic. In fact quite cringe.')
#
#     if message.content.lower() == '$overwatch':
#         await message.channel.send('officially the only move in the discord.')
#

#

#
#     if message.content.lower() == '$whocringe':
#         # response = random.choice(player_names)
#         response = 'Alek'
#         await message.channel.send(response)
#
#     if message.content.lower() == '$move':
#         response = 'Barotrauma'
#         await message.channel.send(response, tts=True)
#
#     if message.content.lower() == '$whoepic':
#         response = random.choice(player_names)
#         await message.channel.send(response)
#
#     if message.content.lower() == '$help':
#         response = 'Commands list: \n\n' \
#                    '`$startup`/`$epiccraft` starts the EC2 server and lists the IP \n' \
#                    '`$shutdown`/`$cringecraft` stops the EC2 server\n' \
#                    '`$addy` lists the current IP\n' \
#                    '`$bounceMcServer` will restart the Minecraft server on the EC2 box\n' \
#                    '`$status` will tell you if the the EC2 server is up or down (doesn\'t know if MC is up) \n' \
#                    '`$howto` will give an overview of how to launch modded minecraft and set your memory\n' \
#                    '`$cost` will print out current monthly cost of AWS service\n' \
#                    '`$backup` will create a backup of today\'s map (can only run if server is up)\n' \
#                    '`$whoup` will print out current player list'
#         await message.channel.send(response)
#



client.run(TOKEN)
