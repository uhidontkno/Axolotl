import json
import discord
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import math
from .libraries.cooldown import Cooldown
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
import random
import io
import os
import base64
import aiohttp
import json
import time
from discord import File
import asyncio

scenes = ["https://www.youtube.com/watch?v=dVOyEEJ4z0I",
          "https://www.youtube.com/watch?v=9O9u9LtVM0o&t=39s",
          "https://www.youtube.com/watch?v=Car_RJJSP1Y",
          "https://www.youtube.com/watch?v=ArGZGAT8rJY",
          "https://www.youtube.com/watch?v=OnJJGtCgok8",
          "https://www.youtube.com/watch?v=EUSFdMonvqs",
          "https://www.youtube.com/watch?v=QVmlWOVa2Cg",
          "https://www.youtube.com/watch?v=7R_1UJkZk2c","https://www.youtube.com/watch?v=_aCGItFCakA"
          ,"https://www.youtube.com/watch?v=GmB1KcH6-iw","https://www.youtube.com/watch?v=boIy4_P6uDI",
          "https://www.youtube.com/watch?v=ji8wr0DjnTA","https://www.youtube.com/watch?v=N9-qEP5nZYA","https://i-just.sold-your.creditcard/sw9i3i28.mp4",
          "https://i-just.sold-your.creditcard/hovq39gz.mp4","https://i-just.sold-your.creditcard/k0o26xit.mp4","https://i-just.sold-your.creditcard/fpipg9gt.mp4",
          "https://i-just.sold-your.creditcard/jjowbw0g.mp4","https://i-just.sold-your.creditcard/y9mnhbzx.mp4"]
scenename = ["I love GD Colon!",
             "INTEL CORE I7-5960X HASWELL-E 8-CORE",
             "Doxxing Squidward",
             "Committing Tax Fraud",
             "Loudward's Confession",
             "THE UNIVERSE IS DYING SPONGEBOB!",
             "PLANKTON JACKS OFF TO THE SECRET FORMULA",
             "PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS",
             "a",
             "I'M GOING TO LOSE IT I'M GOING TO LOSE IT","THIS MESSAGE SHOULD NOT APPEAR","LOUDWARDS WORST STROKE",
             "Loudward Mad","Patrick Smokes Weed","Loudward Pees","Spongebob Exits the simulation","August 12th 2036",
             "Mr Krabs is a Legend!","Spongbob Tries Sax"]

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
        precents = [-10,-3,-2,-1,0,0,1,2,5,10,12,17,24,37,50,69,99,100,420,666,999,42069,69420]
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
        
        precents = [-420,-69,-35,-14,-2,-1,0,1,8,16,32,64,99,100,169,251,269,420,9999]
        await ctx.respond(embed=discord.Embed(title="Annoy Rate fr",color=discord.Color.dark_blue(),description=f"you are {random.choice(precents)}% annoying 💀"), ephemeral=False)
    @commands.slash_command(name="girls-rate", description="how many bitches do you have?")
    async def girlsrate(self, ctx):
       
        precents = ["can't use tinder 💀","can't use tinder 💀","can't use tinder 💀",-1000,-877,-767,-444,-6767,-999,-696,-444,-333,-69,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,4,8,7,6,19,44,358,462,694,42069,69420]
        await ctx.respond(embed=discord.Embed(title="Bitches Rate fr",color=discord.Color.dark_blue(),description=f"you have {random.choice(precents)} bitches"), ephemeral=False)
    @commands.slash_command(name="menrate", description="ayo what the")
    async def menrate(self, ctx):
        await ctx.respond(embed=discord.Embed(title="Men Rate fr",color=discord.Color.dark_blue(),description=f"ay yo what the fuc- no. i'm not doing this"), ephemeral=False)
    @commands.slash_command(
    name="ai-sponge",
    description="i'm dead",
    options=[
        discord.Option(
            name="scene",
            description="Select a scene",
            type=3,
            required=True,
            choices=[
                discord.OptionChoice(value=str(index), name=scenename[index])
                for index, _ in enumerate(scenes)
            ],
        )
    ],
)
    async def aisponge(self, ctx, scene: str):
        scene = int(scene)
        await ctx.respond(content=f"## AI Sponge \n > **Clip Name**: {scenename[scene]}\n > Video: {scenes[scene]}", ephemeral=False)
    @commands.slash_command(name="howmanycrimes", description="Are the police after you?")
    async def crimery(self, ctx, guilty: bool = True): 
       
        emcolor = None
        emtitle = None
        emdescription = None
        crimes = [random.randrange(0,200),random.randrange(0,4),random.randrange(0,17),random.randrange(0,473)]
        if (crimes[0] == 0 and crimes[1] == 0 and crimes[2] == 0 and crimes[3] == 0):
            emcolor = discord.Color.green()
            emtitle = "Woah! Nobody is after you!"
            emfooter = "Congratulations!"
        else:
            emcolor = discord.Color.red()
            emtitle = "Uh Oh."
            emfooter = "Don't worry, there is a **1/694.20 (0.00144%)** chance of being a good boy!"
        emdescription = f'''
Are you a criminal 🤔? Let's find this out!
**You committed**
* Arson {crimes[0]} times
* 🔪 {crimes[1]} times
* Car theft {crimes[2]} times
* Tax Evasion {crimes[3]} times

{emfooter} In total you committed {crimes[0] + crimes[1] + crimes[2] + crimes[3]} crimes.
        '''
        await ctx.respond(embed=discord.Embed(color=emcolor, title=emtitle, description=emdescription))
    @commands.slash_command(name="howmuchbrokeass", description="how much broke ass are you?")
    async def brokerate(self, ctx, user: discord.User = None):
        if not user: user = ctx.author 
        start = -0.5
        end = 1.5
        step = 0.05

        values = []
        current = start
        while current < end:
         values.append(current)
         current += step

        brokepercent = random.choice(values)
        if user != ctx.author:
            directed = f"is {user} a"
            display = f"{user.mention} is"
            md = f"{user.mention} has"
            usrm = f"their"
        else:
            directed = f"are you a"
            display = f"you are"
            md = f"you have"
            usrm = "your"
        await ctx.respond(embed=discord.Embed(title=f"How much {directed} broke ass?",color=discord.Color.dark_blue(),description=f"{display} **{'{:.2f}'.format(brokepercent * -363)}%** broke\n{md} **${'{:.2f}'.format(69420 * brokepercent)}** in {usrm} bank account fr"), ephemeral=False)
    @commands.slash_command(name="ben", description="Talking Ben")
    async def ben(self, ctx, question: str):
        responses = ["Ho Ho Ho!","No.","Yes!","Ugh."]
        file = None
        response = random.choice(responses)
        if "love god" in question.lower():
            response = "Ho Ho Ho... No."
        fp = os.path.join(os.getcwd(), "categories", "assets", "backrooms.mp4")
        backrooms = File(fp)
        fp = os.path.join(os.getcwd(), "categories", "assets", "lean.mp4")
        lean = File(fp)
        if "make lean" in question.lower() :
            file = lean
            response = "..."
        
        elif "backrooms" in question.lower():
            file = backrooms
            response = "..."
        await ctx.respond(content="Starting conversation...",ephemeral=True)
        cem = discord.Embed(color=discord.Color.greyple(), description=f"### Started by {ctx.author.mention}")
        benmsg = await ctx.send(content='''
> **Call started with Talking Ben** 
        ''',embed=cem)
        await asyncio.sleep(2)
        await benmsg.edit(content='''
> **Call started with Talking Ben** 
> Talking Ben: Ben?
        ''',embed=cem)
        await  asyncio.sleep(2)
        await benmsg.edit(content=f'''
> **Call started with Talking Ben** 
> Talking Ben: Ben?
> You: {question}
        ''',embed=cem)
        await asyncio.sleep(2)
        await benmsg.edit(content=f'''
> **Call started with Talking Ben** 
> Talking Ben: Ben?
> You: {question}
> Talking Ben: {response}
> Talking Ben: \*hangs up\*
        ''',embed=cem)
        if file:
         await ctx.respond(file=file)
    @commands.slash_command(name="ask-gpt", description="Ask a question to GPT-3.")
    async def chatgpt(self, ctx, question: str):
        if (len(question) > 1250): 
            await ctx.respond(embed=discord.Embed(color=discord.Color.red(),title="Error",description=f"GPT request error:\nMessage: Prompt too long, shorten it to be under 1250 bytes."))
            return;
         # First, encode the user's question as base64
        question = f'''{question}\n----------
Discord User Info:
Member: {ctx.author}
User ID: {ctx.author.id}
Proper Mention: <@{ctx.author.id}>
Unix Epoch: {time.time()}
----------
Current Server Info:
Name: {ctx.guild.name}
ID: {ctx.guild.id}'''
        encoded_question = base64.b64encode(question.encode("utf-8")).decode("utf-8")
        locations = ["https://bot.noodles.gq","https://c0.noodles.gq","https://c1.noodles.gq","https://c2.noodles.gq","https://c3.noodles.gq","https://delightful-slug-skirt.cyclic.app"]
        # Define the API URL
        API_URL = f"{random.choice(locations)}/bot/ask"

        # Construct the payload data for the API request
        payload = {
            "question": f'''{encoded_question}''',
            "messages": "{}",
            "persona": "You are a helpful GPT-3 based chatbot, you currently live in a discord bot called 'Axolotl'. Axolotl is a custom discord bot written in Python, by rare#3337. Keep in mind that your memory only lasts for one message due to Discord limitations. You have basic access to the current user and guild that you were invoked in, and the info is at the bottom of every message. To mention a user, find the Proper Mention area and use that to mention the user, as that properly pings them on Discord. The current time and date is provided to you in the Unix Epoch. The server that you were invoked in is in the Current Server Info section at the bottom of the message. This section gives the server name and ID."
        }
        
        # Define the headers for the API request
        headers = {
            "Content-Type": "application/json"
        }

        # Defer the slash command while we make the API request
        await ctx.defer()

        # Make the API request using aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, data=json.dumps(payload), headers=headers, timeout=35) as response:
                    if response.status == 200:
                        # Get the response data as plain text
                        response_text = await response.text()
                        if '"error":true' in response_text.lower():
                            errjson = json.loads(response_text)
                            await ctx.respond(embed=discord.Embed(color=discord.Color.red(),title="Error",description=f"GPT request error:\nMessage: {errjson['message']}\nRaw text: `{response_text}`\nServer URL: {API_URL}"))
                            return
                        # Send the response message to the channel
                        await ctx.respond(f"GPT: {response_text}\n\n :information_source: | ||GPT only has a memory lasting for one response due to limitations. To have a proper conversation with GPT, please head over to https://bot.noodles.gq/ or go to the official ChatGPT site: https://chat.openai.com || ")
                    else:
                        # Send an error message if the API request failed
                        await ctx.respond(embed=discord.Embed(color=discord.Color.red(),title="Error",description=f"GPT request error:\nMessage: {response.reason}\nServer URL: {API_URL}"))
                        
        except asyncio.TimeoutError:
            # Send a timeout error message if the API request takes too long
            await ctx.respond(embed=discord.Embed(color=discord.Color.red(),title="Error",description=f"GPT request error:\nMessage: Timed out, url {API_URL} may be down."))
def setup(client):
    client.add_cog(Fun(client))