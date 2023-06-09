import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix="a!", intents=discord.Intents.all())
token = ""

with open("token.env") as f:
    token = f.read().strip()

# Load categories
for filename in os.listdir("./categories"):
    if filename.endswith(".py"):
        client.load_extension(f"categories.{filename[:-3]}")
        print(f"Loaded extension categories.{filename[:-3]}...")

print(f"Loaded all extensions! Logging into discord...")

# Add event handlers
@client.event
async def on_ready():
    # Log a message to indicate that the bot is online
    print("*water swishes*, I'm online!")

@client.event
async def on_slash_command_error(ctx, ex):
    # Log the error message to the console
    print(f"An error occurred while processing slash command in {ctx.guild.id}: {ex}")

# Start the bot
client.run(token)