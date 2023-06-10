import os
import discord
from discord.ext import commands
import time
import sys
client = commands.Bot(command_prefix="!")
token = ""

with open("token.env") as f:
    token = f.read().strip()

# Define dummy slash command
@client.slash_command(name="null")
async def null(ctx: discord.Interaction):
    pass

# Unregister all global slash commands
async def unregister_all_global_commands():
    commands = await client.application.commands.fetch()
    command_ids = [command.id for command in commands if not command.guild_id]
    if command_ids:
        await client.application.commands.delete(*command_ids)
        print(f"Unregistered {len(command_ids)} global slash commands.")
    else:
        print("No global slash commands found.")

# Add event handlers
@client.event
async def on_ready():
    await unregister_all_global_commands()
    print("All global slash commands unregistered.")
    await client.close()

# Start the bot
client.run(token)
print("Closing in 10 sec...")
time.sleep(10)
print("Automatically closing...")
sys.exit(0)
