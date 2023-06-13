import discord
import os
from discord.ext import commands
import threading
import signal
import sys
import asyncio
client = commands.Bot(command_prefix="", intents=discord.Intents.all())
token = ""

with open("token.env") as f:
    token = f.read().strip()

# Load categories
for filename in os.listdir("./categories"):
    if filename.endswith(".py"):
        client.load_extension(f"categories.{filename[:-3]}")
        print(f"Loaded extension categories.{filename[:-3]}...")

print(f"Loaded all extensions! Logging into Discord...")


def run_integrated_server():
    print("SERVER: Starting integrated server...")
    os.system("py categories/flask/integrated-server.py")


# Start the integrated server on a separate thread
server_thread = threading.Thread(target=run_integrated_server)
server_thread.start()


# Add event handlers
@client.event
async def on_ready():
    # Log a message to indicate that the bot is online
    print("*water swishes*, I'm online!")


@client.event
async def on_slash_command_error(ctx, ex):
    # Log the error message to the console
    print(f"An error occurred while processing slash command in {ctx.guild.id}: {ex}")

def stop_bot(signal, frame):
    print("STOP DROP AND ROLL!")
    os.system("taskkill /f /im py.exe")

# Register the signal handler for CTRL+C
signal.signal(signal.SIGINT, stop_bot)



# Start the bot
client.run(token)
