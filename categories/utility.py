import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="pfp", description="Get the avatar of yourself, or others.")
    async def pfp(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        try:
          embed = discord.Embed(title=f"{user.name}'s avatar", color=discord.Color.og_blurple())
          embed.set_image(url=user.avatar.url)

          await ctx.respond(embed=embed)
        except:
          embed = discord.Embed(title=f"{user.name} does not have a profile picture.", color=discord.Color.red())
          await ctx.respond(embed=embed)
    @commands.slash_command(name="ui", description="Get user information.")
    async def user_info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        usrn = user.name
        descrim = user.discriminator
        uid = user.id
        joinepoch = int(user.created_at.timestamp())
        jsepoch = int(user.joined_at.timestamp())
        ifb = user.bot
        embed = discord.Embed(title=f"{user.display_name}'s information", color=discord.Color.blue())
        if ctx.guild.owner.id == uid:
            iso = True
        else:
            iso = False
        embed.description = f"* Bot? {ifb} \n* Owner of server? {iso}\n* Username: {user}\n* Display Name: {user.display_name}\n* User ID: {uid}\n* Join Date: <t:{joinepoch}:R> ( <t:{joinepoch}:F> )\n* Member in server: <t:{jsepoch}:R> ( <t:{jsepoch}:F> )"

        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)

        await ctx.respond(embed=embed)
    @commands.slash_command(name="si", description="Get server information.")
    async def server_info(self, ctx):
        guild = ctx.guild
        gname = guild.name
        sid = guild.id
        mc = guild.member_count
        cepoch = int(guild.created_at.timestamp())
        rc = len(guild.roles)
        tc = len(guild.channels)
        vc = len(guild.voice_channels)
        txtc = len(guild.text_channels)
        bot_count = 0
        member_count = 0
        for member in guild.members:
            if member.bot:
                bot_count += 1
            else:
                member_count += 1
        embed = discord.Embed(title=f"{gname}'s Information", color=discord.Color.og_blurple())

        embed.description = f"""
* Name: {gname}
 * ID: {sid}
* Total Member Count: {mc}
 * Bots: {bot_count}
 * User Count: {member_count}
* Guild Creation Date: <t:{cepoch}:R> ( <t:{cepoch}:F> )
* Roles: {rc - 1}
* Channels: {tc}
 * Voice Channels: {vc}
 * Text Channels: {txtc}"""

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await ctx.respond(embed=embed)
    @commands.slash_command(
        name="every",
        description="List every server the bot is currently in.",
        options=[]
    )
    async def servers(self, ctx):
        # Get a list of all the guild names
        guild_names = [guild.name for guild in self.client.guilds]

        # Join the guild names with a newline character
        servers = "\n".join(guild_names)

        # Get the length of the guilds list
        samt = len(self.client.guilds)

        # Send the response
        response = f"```\n{servers}\n```"
        await ctx.respond(embed=discord.Embed(color=discord.Color.og_blurple(),title=f"Every server I'm inside of ({samt}):",description=f"{response}"), ephemeral = True)
    @commands.slash_command(name="sinv", description="Get the invite link for a server by name.", options=[
    discord.Option(name="sn", description=None, type=3)
])
    async def server_invite(self, ctx: commands.Context, sn: str):
        # Check if the user is the bot owner
        if ctx.author.id != 925430447050207294:
            await ctx.respond("You must be the bot owner to use this command.", ephemeral=True)
            return

        # Find the first guild with the given name
        for guild in self.client.guilds:
            if guild.name.lower() == sn.lower():
                invite_link = await self.create_invite(guild)
                await ctx.respond(invite_link, ephemeral=True)
                return

        await ctx.respond(f"Server not found: {sn}", ephemeral=True)

    async def create_invite(self, guild: discord.Guild) -> str:
        # Get a channel in the server that the bot can create an invite for
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).create_instant_invite:
                invite = await channel.create_invite(max_age=0, max_uses=1)
                return invite.url
def setup(client):
    client.add_cog(Utility(client))