from io import BytesIO
from discord.ext import commands
import discord
import os
import requests
class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Ping the bot")
    async def ping(self, ctx):
        await ctx.response.send_message(content="Pong!", ephemeral=False)
    @commands.slash_command(
        name="invite",
        description="Get the invite link for Axolotl",
    )
    async def sendbotinvite(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Invite Axolotl",
            description="Invite Axolotl to your server by following the below link:\nhttps://discord.com/api/oauth2/authorize?client_id=1116056397608656936&permissions=8&scope=bot%20applications.commands",
            color=0x5865f2
        )
        await ctx.respond(embed=embed, ephemeral=False)
    @commands.slash_command(
        name="status",
        description="View Axolotl's Status",
    )
    async def status(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Axolotl Status",
            description="View Axolotl's status and other IEvade services here: https://stats.uptimerobot.com/PqE16FvrB5",
            color=0x5865f2
        )
        await ctx.respond(embed=embed, ephemeral=False)
    @commands.slash_command(
        name="say-embed",
        description="Say a message, with a embed. (bot owner only)"
    )
    async def semsg(self, ctx: commands.Context, title: str = " ", color: str = None, description: str = " ",content: str = ""):
        if (str(ctx.author.id) != "925430447050207294" and str(ctx.author.id) != "1113660081108684820"):
            await ctx.respond(content="You must be the bot owner to use this command.",ephemeral=True);return
        embed = discord.Embed(
            title=title,
            description=description,
            color=int(color, 16)
        )
        
        await ctx.send(content=content,embed=embed)
        await ctx.respond(content="Done.",ephemeral=True)
    @commands.slash_command(
        name="say",
        description="Say a message (bot owner only)"
    )
    async def smsg(self, ctx: commands.Context, content: str):
        if (str(ctx.author.id) != "925430447050207294" and str(ctx.author.id) != "1113660081108684820"):
            await ctx.respond(content="You must be the bot owner to use this command.",ephemeral=True);return
        await ctx.send(content=content)
        await ctx.respond(content="Done.",ephemeral=True)
    @commands.slash_command(
        name="sayfile",
        description="Send a file. (bot owner only)"
    )
    async def sfile(self, ctx: commands.Context, fileurl: str):
        if str(ctx.author.id) != "925430447050207294":
         await ctx.respond(content="You must be the bot owner to use this command.", ephemeral=True)
         return

        attachment_url = fileurl
        file_request = requests.get(attachment_url)
        file_bytes = BytesIO(file_request.content)
    
        # Get the file extension from the URL
        file_extension = os.path.splitext(attachment_url)[1]
    
        # Create a discord.File object from the BytesIO object
        file = discord.File(file_bytes, filename=f"file{file_extension}")
    
        # Send the file
        await ctx.send(file=file)
    
        await ctx.respond(content="Done.", ephemeral=True)
         
    @commands.slash_command(
        name="nick",
        description="Change the nickname of the bot in the current server (bot owner only)"
    )
    async def nick(self, ctx: commands.Context, nick: str = None):
        if (str(ctx.author.id) != "925430447050207294"):
            await ctx.respond(content="You must be the bot owner to use this command.",ephemeral=True);return
        await ctx.guild.me.edit(nick=nick)
        await ctx.respond(content="Done.",ephemeral=True)
    @commands.slash_command(
        name="help",
        description="Get help with Axolotl",
    )
    async def help(self, ctx: commands.Context):
        # Get the path to the help file
        file_path = os.path.join(os.path.dirname(__file__), "..", "help.md")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            await ctx.respond(f"❌ | Could not find help file (path: {file_path}).", ephemeral=True)
            return
    
        # Try to open the help file
        try:
            with open(file_path, "r") as file:
                help_text = file.read()
        except FileNotFoundError:
            await ctx.respond(f"❌ | Could not find help file.", ephemeral=True)
            return
    
        # Send an ephemeral message with the help text
        embed = discord.Embed(
            title="Axolotl Help",
            description=help_text,
            color=0x5865f2,
        )
        await ctx.respond(embed=embed, ephemeral=True)
def setup(bot):
    bot.add_cog(Other(bot))