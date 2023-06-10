import json
import discord
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import math
from .libraries.cooldown import Cooldown
import requests
import random

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cooldown = Cooldown(15) # Set cooldown to 15 seconds per user by default

    @commands.slash_command(name="crunch-pfp", description="Make your profile picture even funnier.")
    async def crunch_pfp(self, ctx, user: discord.Member = None, crunch: int = 1):
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        
        if user is None:
            user = ctx.author
        if crunch is None:
            crunch = 1
        if crunch > 50:
            await ctx.respond("⚠ | Crunchiness amount must be lower or equal to 50. Setting it to 50.")
            crunch = 50
        if crunch < -10:
            await ctx.respond("⚠ | Crunchiness amount must be higher or equal to -10. Setting it to -10.")
            crunch = -10
        pfp = user.avatar.with_size(512)

        # download the profile picture as bytes
        pfp_bytes = await pfp.read()
        image = Image.open(BytesIO(pfp_bytes))
        image = image.convert("RGB")
        
        # apply filters to the image
        width, height = image.size
        new_width = math.floor(222)
        new_size = (new_width, math.floor(222/2))
        image = image.resize(new_size)
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(math.floor(6.0 + (crunch*2)))
        for i in range(math.floor(6 * ((crunch/2)+1))):
            image = image.filter(ImageFilter.SHARPEN)
        
        # add a red overlay
        red = Image.new("RGBA", image.size, (255, 0, 0, 255))
        red = red.convert("RGB")
        blended = Image.blend(image, red, 0.32)
        image = blended
        image = image.resize((512 * 2, 512),Image.Resampling.NEAREST)
        # save the image to bytes
        with BytesIO() as image_binary:
            image.save(image_binary, 'JPEG', quality=math.floor(16 - (crunch/2)))
            image_binary.seek(0)
            file = discord.File(image_binary, filename='crunch_pfp.jpg')
            await ctx.respond(file=file)

    @commands.slash_command(name="insult", description="Let me ruin your day.")
    async def insult(self, ctx):
        # Check if user is on cooldown
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return

        # Set the user-specific cooldown
        self.cooldown.set_cooldown(ctx.author.id)

        # Fetch insult from API
        response = requests.get("https://insult.mattbas.org/api/insult.txt")
        insult = response.text.strip()

        # Send insult as a response
        await ctx.respond(f"💩 | {insult}", ephemeral=False)
    @commands.slash_command(name="joke", description="Get a random joke!")
    async def joke(self, ctx):
            # Check if user is on cooldown
            cooldown = self.cooldown.get_cooldown(ctx.author.id)
            if cooldown > 0:
                c_minutes = math.floor(cooldown // 60)
                c_seconds = math.floor(cooldown % 60)
                await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message 
                return
    
            # Set the user-specific cooldown
            self.cooldown.set_cooldown(ctx.author.id)
    
            # Fetch joke from API
            response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist&format=txt")
            joke = response.text.strip()
    
            # Send joke as a response
            await ctx.respond(f"😂 | {joke}", ephemeral=False)
    @commands.slash_command(name="cat", description="Get a random cat image or video!")
    async def cat(self, ctx):
                # Check if user is on cooldown
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        json_data = json.loads(response.text)
        image_url = json_data[0]['url']

        embed = discord.Embed(title="🐱 Meow!", color=discord.Color.blue())
        embed.set_image(url=image_url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="dog", description="Get a random dog image or video!")
    async def dog(self, ctx):
                # Check if user is on cooldown
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        response = requests.get("https://api.thedogapi.com/v1/images/search")
        json_data = json.loads(response.text)
        image_url = json_data[0]['url']

        embed = discord.Embed(title="🐶 Woof!", color=discord.Color.blue())
        embed.set_image(url=image_url)
        await ctx.respond(embed=embed)
    @commands.slash_command(name="nuke", description="Obviously destroy a server (FOR OBVIOUS REASONS THIS IS A JOKE)")
    async def nuke(self, ctx):
        await ctx.respond("✅ | Successfully nuked! (jk jk)", ephemeral=True)
    @commands.slash_command(name="gayrate", description="how gay are you fr fr")
    async def gayrate(self, ctx):
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        precents = [-1,0,1,2,5,10,12,17,24,37,50,69,99,100,420,666,999,42069,69420]
        await ctx.respond(embed=discord.Embed(title="Gay Rate fr",color=discord.Color.dark_blue(),description=f"you are {random.choice(precents)}% gay fr 😳"), ephemeral=False)
    @commands.slash_command(name="rizzrate", description="how much rizz do you have 😈")
    async def rizzrate(self, ctx):
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        precents = [-1,0,1,2,5,10,12,17,24,37,50,69,99,100,420,666,999,42069,69420]
        await ctx.respond(embed=discord.Embed(title="Rizz Rate fr",color=discord.Color.dark_blue(),description=f"you have {random.choice(precents)}% rizz 😈😮‍💨"), ephemeral=False)
    @commands.slash_command(name="racistrate", description="how racist are you? 💀")
    async def racistrate(self, ctx):
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        precents = [-1,0,1,2,5,10,12,17,24,37,50,69,99,100,420,666,999,42069,69420]
        await ctx.respond(embed=discord.Embed(title="Racist Rate fr",color=discord.Color.dark_blue(),description=f"you are {random.choice(precents)}% racist 💀"), ephemeral=False)
    @commands.slash_command(name="annoyrate", description="how annoying are you?")
    async def annoyrate(self, ctx):
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        precents = [-420,-69,-35,-14,-2,-1,0,1,8,16,32,64,99,100,169,251,269,420,9999]
        await ctx.respond(embed=discord.Embed(title="Annoy Rate fr",color=discord.Color.dark_blue(),description=f"you are {random.choice(precents)}% annoying 💀"), ephemeral=False)
    @commands.slash_command(name="girlsrate", description="how many bitches do you have?")
    async def annoyrate(self, ctx):
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
            c_minutes = math.floor(cooldown // 60)
            c_seconds = math.floor(cooldown % 60)
            await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True) # respond with error message
            return
        precents = ["can't use tinder 💀","can't use tinder 💀",-999,-696,-444,-333,-69,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,4,8,7,6,19,44,358,462,694,42069,69420]
        await ctx.respond(embed=discord.Embed(title="Bitches Rate fr",color=discord.Color.dark_blue(),description=f"you have {random.choice(precents)} bitches"), ephemeral=False)
def setup(client):
    client.add_cog(Fun(client))