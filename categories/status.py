import random
import discord
from discord.ext import tasks, commands
import asyncio
class Status(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.presences = [
            (discord.ActivityType.playing, "with my pet axolotl"),
            (discord.ActivityType.watching, "my axolotl swim"),
            (discord.ActivityType.playing, "Minecraft"),
            (discord.ActivityType.listening, "to Minecraft music"),
            (discord.ActivityType.playing, "with other axolotls"),
            (discord.ActivityType.watching, "axolotls swim around my tank!"),
            (discord.ActivityType.listening, "to Subnautica music"),
            (discord.ActivityType.playing, "the new Minecraft 1.20 update."),
        ]
        self.status_types = [
            discord.Status.online,
            discord.Status.idle,
            discord.Status.do_not_disturb
        ]
        print("STATUS: Waiting until bot is ready")

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(seconds=45)
    async def change_status(self):
        presence_type, presence_text = random.choice(self.presences)
        status = random.choice(self.status_types)
        activity = discord.Activity(type=presence_type, name=presence_text)
        await self.client.change_presence(status=status, activity=activity)
    @commands.Cog.listener()
    async def on_ready(self):
        
        await self.client.wait_until_ready() # Wait until bot is ready
        await asyncio.sleep(3) 
        print("STATUS: Started cycling through statuses")
        self.change_status.start() # Start the loop

def setup(client):
    client.add_cog(Status(client))