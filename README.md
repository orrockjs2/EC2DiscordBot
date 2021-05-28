# EC2DiscordBot
Python repo for Discord bot that interacts with EC2 server

# Secrets and Requirements
You will need a .env file with your bot's Token, this is found on the Bot section of your discord app page, under 'Token'
Additionally, an EC2 instance with appropriate perms, read about security for an EC2 and connecting to one here: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstances.html

you will also need an instance_id.txt file with your ec2 instance id


### TODO:

    1. Add IP output to bot --done
    2. Add startup/shutdown to bot -- done
    3. Write minecraft startup.sh script -- done
    4. See if the discord bot can call the startup.sh script or if it can be automated on server startup -- calling script done --automated on startup
    5. figure out how to persist data between stop and start (the script, MC world, etc) -- going to do this with auto backups to my WSL2 machine --done
    6. upgrade server to 8Gib
    7. Make sure world and stuff gets persisted -- i think this is good minecraft default saves every 5 mins
    8. change memory params on minecraft.sh
    9. mod server
    10. Run backup on every startup