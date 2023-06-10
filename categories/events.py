import os
from discord import File
from discord.ext import commands
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "darkspeed" in message.content.lower():
            file_path = os.path.join(os.getcwd(), "categories", "assets", "lego-breaking.mp3")
            file = File(file_path)
            msg = await message.channel.send(content="darkspeed equals:", file=file)
            await msg.add_reaction("🇫")
            await msg.add_reaction("🇷")
        if "proxy civil" in message.content.lower():
            file_path = os.path.join(os.getcwd(), "categories", "assets", "lego-breaking.mp3")
            file = File(file_path)
            msg = await message.channel.send(content="proxy civilization is the most :regional_indicator_l: server out there, don't join! the owner steals ads and the server is poorly put together, its a great value clone of ievade central, proxy civilization equals:", file=file)
            await msg.add_reaction("🇫")
            await msg.add_reaction("🇷")
        if "grammar" in message.content.lower():
            file_path = os.path.join(os.getcwd(), "categories", "assets", "grammarlyad_compressed.mp4")
            file = File(file_path)
            msg = await message.channel.send(file=file)
            await msg.add_reaction("🇴")
            await msg.add_reaction("🇳")
            await msg.add_reaction("🇬")

def setup(bot):
    bot.add_cog(Events(bot))