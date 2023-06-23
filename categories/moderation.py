import discord
from discord.ext import commands
import time
import math
import random
import datetime
import re
import asyncio
from discord.ext.commands import MissingPermissions
strings = ['haha','lmao','very much a sped user',
               '<https://dont-get.trolled.host/s/yv5jxeoita>',
               'cope harder','okay shrek','i dont like you',
               'ooooooooooh he got caught','i hate you','don\'t do it again',
               'heheheha','https://dont-get.trolled.host/ccebvjbx.mp3','bum ahh']
class Moderation(commands.Cog):

  
    def __init__(self, bot):
        self.bot = bot
 
    @commands.slash_command(name="warn",
                            description="Warn a user with a reason",
                            options=[ discord.Option(name="user", description="The user to warn", type=3),
                                      discord.Option(name="reason", description="The reason for the warning", type=3)])
    async def warn(self, ctx: commands.Context, user: str, reason: str = "No reason specified."):
        # Check if the user has the necessary permissions
        user = user.strip()

        if not ctx.author.guild_permissions.kick_members:
            await ctx.respond(f"❌ | You do not have permission to use the `/warn` command.", ephemeral=True)
            return

        # Find the user object using the username or nickname
        user = discord.utils.get(ctx.guild.members, mention=user)
        if not user:
            await ctx.respond("❌ | Invalid user.", ephemeral=True)
            return

        # Check if the user is a bot or cannot be DM'd
        if user.bot:
            await ctx.respond("❌ | Cannot warn a bot.", ephemeral=True)
            return

        try:
            # Create the warning embed
            embed = discord.Embed(title="⚠ | WARNING", description=f"You have been warned in **{ctx.guild.name}**!\nReason given: **{reason}**", color=discord.Color.green())
            embed.add_field(name="\u200b", value=f"{strings[random.randrange(len(strings))]} | At: <t:{math.floor(time.time())}:f> | By: {ctx.author} ({ctx.author.mention})", inline=True)

            # Send a warning message to the user
            await user.send(embed=embed)

            # Send a confirmation message in the channel
            await ctx.respond(f"✅ | {user.mention} has been warned. Reason: {reason}", ephemeral=True)

        except discord.Forbidden:
            await ctx.respond(f"✅ | {user.mention} has been warned. Reason: {reason}", ephemeral=True)
            await ctx.respond("❌ | Could not send DM to user.", ephemeral=True)

    @commands.slash_command(
        name="kick",
        description="Kick a user with a reason",
        options=[
            discord.Option(name="user",description="The user to kick (username, username#discriminator, user ID, or mention)",type=3),
            discord.Option(name="reason",description="The reason for the kick",type=3)]
    )
    async def kick(self, ctx: commands.Context, user: str, reason: str = "No reason specified."):
        user = user.strip()
        if not ctx.author.guild_permissions.kick_members:
            await ctx.respond(f"❌ | You do not have permission to use the `/kick` command.", ephemeral=True)
            return
        try:
            member = await commands.MemberConverter().convert(ctx, user)
        except commands.errors.BadArgument:
            member = None
        if not member:
            await ctx.respond(f"❌ | Invalid user. (User Param {user})", ephemeral=True)
            return
        user = await self.bot.fetch_user(member.id)
        if not user:
            await ctx.respond(f"❌ | Could not find user. (ID: {member.id}, User Param {user})", ephemeral=True)
            return
        embed = discord.Embed(title="👢 | KICKED", description=f"You have been kicked in **{ctx.guild.name}**!\nReason given: **{reason}**", color=discord.Color.dark_orange())
        embed.add_field(name="\u200b", value=f"{strings[random.randrange(len(strings))]} | At: <t:{math.floor(time.time())}:f> | By: {ctx.author} ({ctx.author.mention})", inline=True)
        await user.send(embed=embed)
        await member.kick(reason=reason)
        await ctx.respond(f"✅ | User {member.mention} has been kicked. Reason: {reason}", ephemeral=True)
    @commands.slash_command(
        name="ban",
        description="Ban a user with a reason",
        options=[
            discord.Option(
                name="user",
                description="The user to ban (username, username#discriminator, user ID, or mention)",
                type=3,
                required=True
            ),
            discord.Option(
                name="reason",
                description="The reason for the ban",
                type=3,
                required=False
            )
        ]
    )
    async def ban(self, ctx: commands.Context, user: str, reason: str = "No reason specified."):
        user = user.strip()
    
        # Check if the user has the necessary permissions
        if not ctx.author.guild_permissions.ban_members:
            await ctx.respond(f"❌ | You do not have permission to use the `/ban` command.", ephemeral=True)
            return
    
        # Convert the user parameter to a discord.Member object
        try:
            member = await commands.MemberConverter().convert(ctx, user)
        except commands.errors.BadArgument:
            member = None
    
        if not member:
            await ctx.respond(f"❌ | Invalid user. (User Param {user})", ephemeral=True)
            return
    
        user_obj = await self.bot.fetch_user(member.id)
        if not user_obj:
            await ctx.respond(f"❌ | Could not find user. (ID: {member.id}, User Param {user})", ephemeral=True)
            return
    
        embed = discord.Embed(
            title="🔨 | BANNED",
            description=f"You have been banned in **{ctx.guild.name}**!\nReason given: **{reason}**",
            color=discord.Color.red()
        )
        embed.add_field(name="\u200b", value=f"{strings[random.randrange(len(strings))]} | At: <t:{math.floor(time.time())}:f> | By: {ctx.author} ({ctx.author.mention})", inline=True)
        await user_obj.send(embed=embed)
    
        await member.ban(reason=reason)
    
        await ctx.respond(f"✅ | User {member.mention} has been banned. Reason: {reason}", ephemeral=True)
    @commands.slash_command(
        name="purge",
        description="Purge a specific number of messages",
        options=[
            discord.Option(
                name="messages",
                description="The number of messages to purge (default: 10, max: 100)",
                type=4,
                required=False
            )
        ]
    )
    async def purge(self, ctx: commands.Context, messages: int = 10):
        # Check if the user has the necessary permissions
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.respond(f"❌ | You do not have permission to use the `/purge` command.", ephemeral=True)
            return
    
        # Convert messages_num to an integer
        try:
            messages_num = int(messages)
        except:
            await ctx.respond(f"⚠ | Message count not defined or not an integer. Defaulting to 10.", ephemeral=True)
            messages_num = 10
    
        # Check if messages_num is between 1 and 100
        if messages_num < 1:
            messages_num = 1
        elif messages_num > 100:
            messages_num = 100
    
        # Purge the specified number of messages
        deleted_messages = await ctx.channel.purge(limit=messages_num)
    
        # Send a confirmation message in the channel
        await ctx.respond(f"✅ | Purged {len(deleted_messages)} messages!", ephemeral=True)
    @commands.slash_command(
        name="mute",
        description="Mute a user using Discord's timeout feature",
        options=[
            discord.Option(
                name="user",
                description="The user to mute (username, username#discriminator, user ID, or mention)",
                type=3,
                required=True
            ),
            discord.Option(
                name="length",
                description="The length of the mute (format: [number][s/m/h/d/w], e.g. 1s, 2m, 3h, 4d, 5w)",
                type=3,
                required=True
            ),
            discord.Option(
                name="reason",
                description="The reason for the mute",
                type=3,
                required=False
            )
        ]
    )
    async def mute(self, ctx: commands.Context, user: str, length: str, reason: str = "No reason specified."):
        # Check if the user has the necessary permissions
        if not ctx.author.guild_permissions.moderate_members:
            await ctx.respond(f"❌ | You do not have permission to use the `/mute` command.", ephemeral=True)
            return
    
        # Convert the length parameter to seconds
        duration_units = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
            "w": 604800
        }
        try:
            duration = int(length[:-1]) * duration_units[length[-1]]
        except KeyError:
            await ctx.respond(f"❌ | Invalid length format. The format should be in the form of [number][s/m/h/d/w].", ephemeral=True)
            return
    
        # Check if the length is within the allowed range
        if duration < 60 or duration > 604800:
            await ctx.respond(f"❌ | The length of the mute must be between 60 seconds and 7 days.", ephemeral=True)
            return
    
        # Convert the user parameter to a discord.Member object
        try:
            member = await commands.MemberConverter().convert(ctx, user)
        except commands.errors.BadArgument:
            member = None
        if not member:
            await ctx.respond(f"❌ | Invalid user. (User Param {user})", ephemeral=True)
            return
    
        # DM the user
        user_obj = await self.bot.fetch_user(member.id)
        if not user_obj:
            await ctx.respond(f"❌ | Could not find user. (ID: {member.id}, User Param {user})", ephemeral=True)
            return
    
        embed = discord.Embed(
            title="🔇 | MUTED",
            description=f"You have been muted in **{ctx.guild.name}** for {length}. Reason given: **{reason}**",
            color=discord.Color.gold()
        )
        embed.add_field(name="\u200b", value=f"{strings[random.randrange(len(strings))]} | At: <t:{math.floor(time.time())}:f> | By: {ctx.author} ({ctx.author.mention})", inline=True)
        embed.set_footer(text="This mute will automatically expire when the time is up.")
        await user_obj.send(embed=embed)
    
        # Mute the user using Discord's timeout feature
       # await member.edit(mute=True, reason=reason)
        await member.timeout_for(datetime.timedelta(seconds=duration))
    
        # Send a confirmation message in the channel
        await ctx.respond(f"✅ | User {member.mention} has been muted for {length}. Reason: {reason}", ephemeral=True)
    @commands.slash_command(
        name="unmute",
        description="Unmute a user using Discord's timeout feature",
        options=[
            discord.Option(
                name="user",
                description="The user to mute (username, username#discriminator, user ID, or mention)",
                type=3,
                required=True
            ),
            discord.Option(
                name="reason",
                description="The reason for the mute",
                type=3,
                required=False
            )
        ]
    )
    async def unmute(self, ctx: commands.Context, user: str, reason: str = "No reason specified."):
        # Check if the user has the necessary permissions
        if not ctx.author.guild_permissions.timeout_members:
            await ctx.respond(f"❌ | You do not have permission to use the `/unmute` command.", ephemeral=True)
            return
    
    
        # Convert the user parameter to a discord.Member object
        try:
            member = await commands.MemberConverter().convert(ctx, user)
        except commands.errors.BadArgument:
            member = None
        if not member:
            await ctx.respond(f"❌ | Invalid user. (User Param {user})", ephemeral=True)
            return
    
        # DM the user
        user_obj = await self.bot.fetch_user(member.id)
        if not user_obj:
            await ctx.respond(f"❌ | Could not find user. (ID: {member.id}, User Param {user})", ephemeral=True)
            return
    
        embed = discord.Embed(
            title="🔉 | UNMUTED",
            description=f"You have been unmuted in **{ctx.guild.name}**! Reason given: **{reason}**",
            color=discord.Color.green()
            
        )
        embed.add_field(name="\u200b", value=f"yippee! | At: <t:{math.floor(time.time())}:f> | By: {ctx.author} ({ctx.author.mention})", inline=True)
        
        await user_obj.send(embed=embed)
    
        # Mute the user using Discord's timeout feature
       # await member.edit(mute=True, reason=reason)
        await member.remove_timeout()
    
        # Send a confirmation message in the channel
        await ctx.respond(f"✅ | User {member.mention} has been unmuted.", ephemeral=True)
    @commands.slash_command(
        name="unban",
        description="Unban a user from the server",
        options=[
            discord.Option(
                name="user",
                description="The user to unban (username, username#discriminator, user ID, or mention)",
                type=3,
                required=True
            ),
            discord.Option(
                name="reason",
                description="The reason for the unban",
                type=3,
                required=False,
                default="No reason specified."
            )
        ]
    )
    async def unban(self, ctx: commands.Context, user: str, reason: str = "No reason specified."):
        # Check if the user has the necessary permissions
        if not ctx.author.guild_permissions.ban_members:
            await ctx.respond(f"❌ | You do not have permission to use the `/unban` command.", ephemeral=True)
            return
    
        # Convert the user parameter to a discord.User object
        try:
            user_obj = await commands.UserConverter().convert(ctx, user)
        except commands.errors.BadArgument:
            await ctx.respond(f"❌ | Invalid user. (User Param {user})", ephemeral=True)
            return
    
        # Unban the user
        await ctx.guild.unban(user_obj, reason=reason)
    
        # Send a DM to the unbanned user (if possible)
        try:
            embed = discord.Embed(
                title="✅ | You've been unbanned",
                description=f"You have been unbanned in **{ctx.guild.name}**!\nReason given: **{reason}**",
                color=discord.Color.green()
            )
            await user_obj.send(embed=embed)
        except discord.errors.Forbidden:
            pass
        
        # Send a confirmation message in the channel
        if reason:
            await ctx.respond(f"✅ | User {user_obj.mention} has been unbanned. Reason: {reason}", ephemeral=True)
        else:
            await ctx.respond(f"✅ | User {user_obj.mention} has been unbanned.", ephemeral=True)
    @commands.slash_command(
        name="slowmode",
        description="Set the slow mode for the current channel",
        options=[
            discord.Option(
                name="time",
                description="The slow mode time (0 to 6h, e.g. 3m30s)",
                type=3,
                required=True
            )
        ]
    )
    async def slowmode(self, ctx: commands.Context, time: str):
        # Define the minimum and maximum slow mode times
        min_time = 0
        max_time = 6 * 60 * 60
    
        # Parse the time string to seconds
        regex = re.compile(r"(\d+)(s|m|h)?")
        segments = regex.findall(time)
        seconds = sum(int(num) * {"s": 1, "m": 60, "h": 60 * 60}.get(unit, 1) for num, unit in segments)
    
        # Set the slow mode time for the channel, or disable slowmode if the time is 0
        if seconds == min_time:
            await ctx.channel.edit(slowmode_delay=0)
        elif seconds < min_time or seconds > max_time:
            await ctx.respond(f"❌ | Error: Slow mode time must be between 0 and 6 hours.", ephemeral=True)
            return
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
    
        # Send a success message
        if seconds == min_time:
            embed = discord.Embed(
                title="✅ | Success",
                description="Successfully disabled the slow mode!",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="✅ | Success",
                description=f"Successfully set the slow mode to `{time}`!",
                color=discord.Color.green()
            )
        await ctx.respond(embed=embed, ephemeral=True)
   
    @commands.slash_command(name="lock", description="Lock the channel")
    async def lock(self, ctx: commands.Context, reason: str = "No reason specified."):
        channel = ctx.channel
        bot = ctx.guild.me
    
        try:
            # Check if the user and bot have the manage_channels permission
            if not channel.permissions_for(ctx.author).manage_channels or not channel.permissions_for(bot).manage_channels:
                await ctx.respond("Both you and the bot must have the 'Manage Channels' permission to use this command.", ephemeral=True)
                return
    
            # Disable sending messages for @everyone
            await channel.set_permissions(ctx.guild.default_role, send_messages=False, send_messages_in_threads=False)
    
            # Send lock message
            embed = discord.Embed(title="🔒 | Channel Lockdown", description=f"{channel.mention} has been locked. \n **Reason**: \n{reason}", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=False)
    
        except Exception as e:
            await ctx.respond(f"You / bot may be missing {e.missing_perms} permission(s) to run this command.", ephemeral=True)
    
    @commands.slash_command(name="unlock", description="Unlock the channel")
    async def unlock(self, ctx: commands.Context, reason: str = "No reason specified."):
        channel = ctx.channel
        bot = ctx.guild.me
    
        try:
            # Check if the user and bot have the manage_channels permission
            if not channel.permissions_for(ctx.author).manage_channels or not channel.permissions_for(bot).manage_channels:
                await ctx.respond("Both you and the bot must have the 'Manage Channels' permission to use this command.", ephemeral=True)
                return
    
            # Enable sending messages for @everyone
            await channel.set_permissions(ctx.guild.default_role, send_messages=True, send_messages_in_threads=True)
    
            # Send unlock message
            embed = discord.Embed(title="🔓 | Channel Unlock", description=f"{channel.mention} has been unlocked. \n **Reason**: \n{reason}", color=discord.Color.green())
            await ctx.respond(embed=embed, ephemeral=False)
    
        except Exception as e:
            await ctx.respond(f"You / bot may be missing {e.missing_perms} permission(s) to run this command.", ephemeral=True)
    

def setup(bot):
    bot.add_cog(Moderation(bot))