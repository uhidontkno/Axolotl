from discord.ext import commands
import discord
import os

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
    async def invite(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Invite Axolotl",
            description="Invite Axolotl to your server by following the below link:\nhttps://discord.com/api/oauth2/authorize?client_id=1116056397608656936&permissions=8&scope=bot%20applications.commands",
            color=0x5865f2
        )
        await ctx.respond(embed=embed, ephemeral=True)
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