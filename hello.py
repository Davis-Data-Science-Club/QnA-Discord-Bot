import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ROLE_ID = os.getenv("ROLE_ID")

#Specify what type of access the bot will have. In our case, all.
intents = discord.Intents.all()
intents.members = True

#Creates a new discord Bot
bot = commands.Bot(command_prefix="!", intents=intents)

#Event handler that prints "Logged in" when the discord bot is up and running.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

ratings = {}

#placeholder function for nltk portion
def example_function(input):
    if input == "Freeze!":
        return
    return input

#Bot command that is triggered using !q, will call the function and output a response. 
@bot.command()
async def q(ctx, *, question):
    response = example_function(question)
    if response is None:
        await ctx.send("Sorry, I couldn't find an answer to that question.")
        role = ctx.guild.get_role(ROLE_ID)
        await ctx.send("Maybe an " + role.mention + " can help you out.")
    else:
        await ctx.send(response)
        # Ask the user to rate the response
        await ctx.send("Please rate my response from 1 to 10.")
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit()

        # Wait for the user's rating
        try:
            rating = await bot.wait_for("message", check=check, timeout=10.0)
            rating_value = int(rating.content)
            if rating_value < 1 or rating_value > 10:
                await ctx.send("Invalid rating. Please enter a number between 1 and 10.")
            else:
                # Store the question, response, and rating
                ratings[(ctx.author.name, question, response)] = rating_value
                await ctx.send("Thank you for your rating.")
        except asyncio.TimeoutError:
            await ctx.send("You did not enter a rating. Rating will not be recorded.")

        # Write the ratings to a file
        with open("ratings.txt", "a") as file:
            file.write(f"{ctx.author.name}, {question}, {response}, {rating_value}\n")

bot.run(DISCORD_TOKEN)
