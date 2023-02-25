import discord

#Specify what type of access the bot will have. In our case, all.
intents = discord.Intents.all()
intents.members = True

#Creates a new discord client
client = discord.Client(intents=intents)

#Event handler that prints "Logged in" when the discord bot is up and running.
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

#Event handler that receives a message and replies "hello" to any user input. 
#It handles conditional logic such that message inputs hi or hello responds hello with the user's discord name. 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == "hello" or "hi":
        await message.channel.send(f"Hello {message.author.name}!")
    else:
        await message.channel.send("Hello!")

client.run('BOT_TOKEN')
