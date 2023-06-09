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
def setup(client):
    client.add_cog(Utility(client))