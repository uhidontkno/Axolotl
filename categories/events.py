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
            msg = await message.channel.send(content="writing not easy, but grammarly can help! This sentence is grammatically correct, but wordy and hard-to-read.",file=file)
            await msg.add_reaction("🇴")
            await msg.add_reaction("🇳")
            await msg.add_reaction("🇬")
        if "ievade" in message.content.lower():
            msg = await message.channel.send(content="IEvade best server fr fr most :regional_indicator_w: bypassing server")
            await msg.add_reaction("🇼")
        if "pride month" in message.content.lower():
            file_path = os.path.join(os.getcwd(), "categories", "assets", "pride-month.mp4")
            file = File(file_path)
            msg = await message.channel.send(content="fuck pride month",file=file)
        if "never pirate" in message.content.lower():
            msg = await message.channel.send(content="my son will never pirate south park\nhttps://files.basketcraft.net/christmaspoo-lg.mp4")
        if "light mode" in message.content.lower():
            msg = await message.channel.send(content="my eyes hurt already")
        if "discord light mode" in message.content.lower():
            msg = await message.channel.send(content="https://www.youtube.com/watch?v=XlgqZeeoOtI")
        if "discord light theme" in message.content.lower():
            msg = await message.channel.send(content="https://www.youtube.com/watch?v=XlgqZeeoOtI")
        if "dark mode" in message.content.lower():
            msg = await message.channel.send(content="gimme gimme mine mine mine mine mine mine!!!!")

def setup(bot):
    bot.add_cog(Events(bot))