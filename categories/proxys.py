import discord
from discord.ext import commands
import os
import random
import sys
import math
import requests
import asyncio
import discord.ui
from typing import Dict
from .libraries.cooldown import Cooldown
proxy_dir = "proxies"
proxy_types = [
          "artclass",
          "emerald",
          "holy-unblocker",
          "interstellar",
          "ludicrous",
          "nebula",
          "rammerhead",
          "shuttle",
           "tiw",
           "ultraviolet",
           "void",
           "jordans-math-work",
           "incognito",
           "noodles",
           "noodlegpt",
           "bigfoot",
           "utopia",
        ]
p_c = {"artclass":"discord.gg/desmos",
               "nebula":"discord.gg/unblocker",
               "ultraviolet":"discord.gg/unblock",
               "tiw":"discord.gg/8dUtxmw8sv",
               "interstellar":"discord.gg/gointerstellar",
               "shuttle":"discord.gg/xi",
               "emerald":"discord.gg/Mvc67DmT4C",
               "holy-unblocker":"discord.gg/unblock",
               "rammerhead":"discord.gg/VNT4E7gN5Y",
               "ludicrous":"discord.gg/unblock",
               "void":"N/A"}

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Save to DMs", style=discord.ButtonStyle.gray) 
    async def button_callback(self, button, interaction):
        description = interaction.message.embeds[0].description
        start_idx = description.find("###")
        if start_idx != -1:
         url = description[start_idx+3:].strip()
        else:
         url = "Failed to fetch."
        try:
          await interaction.user.send(embed=discord.Embed(title="Here's your proxy!", description=f"### {url}", color=discord.Color.blue()))
          await interaction.response.send_message(content="Check your DMs!",ephemeral=True)
        except:
          await interaction.response.send_message(content="Failed to DM. Please check to see if you have DMs enabled.",ephemeral=True)

class dispView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a proxy to dispense.", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
         
            discord.SelectOption(    
                label="Artclass",value="artclass"
            ),
            
            discord.SelectOption(
                label="Emerald",value="emerald"
            ),
            discord.SelectOption(
                label="Holy Unblocker",value="holy-unblocker"
            ),
            discord.SelectOption(
                label="Interstellar",value="interstellar"
            ),
            discord.SelectOption(
                label="Ludicrous",value="ludicrous"
            ),
            discord.SelectOption(
                label="Nebula",value="nebula"
            ),
            discord.SelectOption(
                label="Rammerhead",value="rammerhead"
            ),
            discord.SelectOption(
                label="Shuttle",value="shuttle"
            ),
            discord.SelectOption(
                label="TIW",value="tiw"
            ),
            discord.SelectOption(
                label="Ultraviolet",value="ultraviolet"
            ),
            discord.SelectOption(
                label="Void",value="void"
            ),
            discord.SelectOption(
                label="Jordans Math Work",value="jordans-math-work"
            ),
            discord.SelectOption(
                label="Incognito",value="incognito"
            ),
            discord.SelectOption(
                label="Noodle Games",value="noodles"
            ),
            discord.SelectOption(
                label="Noodle GPT",value="noodlegpt"
            ),
        ]
        
    )

           #  "jordans-math-work",
         #  "incognito",
          # "noodles",
          # "noodlegpt",
          # "bigfoot",
          # "utopia",

    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        cooldown = Proxys.cooldown.get_cooldown(interaction.user.id)
        if cooldown > 0:
          c_minutes = math.floor(cooldown // 60)
          c_seconds = math.floor(cooldown % 60)
          await interaction.response.send_message(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True)
          return

        # Set the user-specific cooldown
        Proxys.cooldown.set_cooldown(interaction.user.id)
        with open(os.path.join(proxy_dir,f"{select.values[0]}.txt"), "r") as file:
            proxies = [proxy.strip().replace(" ", "-") for proxy in file.readlines()]
        if len(proxies) == 0:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ | Error",
                    description=f'No proxies available for {select.values[0]}.',
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
        proxy = random.choice(proxies).strip()

        warning = ""
        if (select.values[0] == "emerald"):
            warning = '''\n
## ⚠ | WARNING
**Emerald proxies always go down during the summer, so if you are doing summer school virtually, emerald proxies will not work for you until school starts.**
'''
        elif (select.values[0] == "void"):
            warning = '''\n
## ⚠ | WARNING
**Void proxies currently do not work at the moment. (Updated 6/8/23)**
'''
        if p_c[select.values[0]] != "N/A":
            dpm = await interaction.response.send_message(
                embed=discord.Embed(
                     title="\🌐 | Here's your proxy",
                     description=f"### **{proxy}** \n{warning}\nJoin {select.values[0]}'s official discord server for support: https://{p_c[select.values[0]]}",
                     color=discord.Color.green(),
                 ).set_footer(text="Come back in 15 minutes to get another one!"),
                 view=MyView(),
                 ephemeral=True
            )
        else:
            dpm = await interaction.response.send_message(
                embed=discord.Embed(
                     title="\🌐 | Here's your proxy",
                     description=f"### **{proxy}** \n{warning}",
                     color=discord.Color.green(),
                 ).set_footer(text="Come back in 15 minutes to get another one!"),
                 view=MyView(),
                 ephemeral=True
            )
        me = await interaction.followup.send(
                embed=discord.Embed(
                     title="\🌐 | Checking your proxy...",
                     description=f"",
                     color=discord.Color.blue(),
                 ),
                 ephemeral=True,
            )  
        ppr = await check_proxy(proxy)
        await me.edit(embed=ppr)


class Proxys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cooldown = Cooldown(900)  # 15 secs due to debug, but 15 * 60 is what you need
    cooldown = Cooldown(900)
    @commands.slash_command(name="disp-panel")
    async def pdp(self,ctx: commands.Context):
      if (str(ctx.guild.id) == "1101109470454632518" and ctx.author.guild_permissions.administrator):
       await ctx.send(embed=discord.Embed(title="Proxy Dispenser",color=discord.Color.green(),description="Select one of the proxy types below to get one. 15 minute cooldown."), view=dispView())
       await ctx.respond("Panel has been sent in the current channel.",ephemeral=True)
      else:
       await ctx.respond("Command must be used in IEvade Central and you must have Adminstrator permissions.",ephemeral=True)



    @commands.slash_command(
        name="proxy",
        description="Get a random proxy from the specified type.",
        options=[
            discord.Option(
                name="type",
                description="The type of proxy to give.",
                type=3,
                required=True,
                choices=[discord.OptionChoice(value=proxy_type, name=proxy_type) for proxy_type in proxy_types],
            )
        ],
    )
    async def proxy_command(self, ctx: commands.Context, type: str):
        cooldown = self.cooldown.get_cooldown(ctx.author.id)
        if cooldown > 0:
          c_minutes = math.floor(cooldown // 60)
          c_seconds = math.floor(cooldown % 60)
          await ctx.respond(f"❌ | You're on a cooldown. Try again in {c_minutes} minutes and {c_seconds} seconds.", ephemeral=True)
          return

        # Set the user-specific cooldown
        self.cooldown.set_cooldown(ctx.author.id)
   
        if type not in proxy_types:
            await ctx.respond(
                embed=discord.Embed(
                    title="❌ | Error",
                    description=f"`{type}` is not a recognized proxy type.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
        file_path = os.path.join(proxy_dir, f"{type.strip().replace(' ', '-')}.txt")
        if not os.path.isfile(file_path):
            await ctx.respond(
                embed=discord.Embed(
                    title="❌ | Error",
                    description=f"No proxies available for {type}.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
    
        with open(file_path, "r") as file:
            proxies = [proxy.strip().replace(" ", "-") for proxy in file.readlines()]
        if len(proxies) == 0:
            await ctx.respond(
                embed=discord.Embed(
                    title="❌ | Error",
                    description=f'No proxies available for {type}.',
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
        proxy = random.choice(proxies).strip()
        warning = ""
        if (type == "Emerald"):
            warning = '''\n
## ⚠ | WARNING
**Emerald proxies always go down during the summer, so if you are doing summer school virtually, emerald proxies will not work for you until school starts.**
'''
        elif (type == "Void"):
            warning = '''\n
## ⚠ | WARNING
**Void proxies currently do not work at the moment. (Updated 6/8/23)**
'''
        if p_c[type] != "N/A":
            dpm = await ctx.respond(
                embed=discord.Embed(
                     title="\🌐 | Here's your proxy",
                     description=f"### **{proxy}** \n{warning}\nJoin {type}'s official discord server for support: https://{p_c[type]}",
                     color=discord.Color.green(),
                 ).set_footer(text="Come back in 15 minutes to get another one!"),
                 view=MyView(),
                 ephemeral=True
            )
        else:
            dpm = await ctx.respond(
                embed=discord.Embed(
                     title="\🌐 | Here's your proxy",
                     description=f"### **{proxy}** \n{warning}",
                     color=discord.Color.green(),
                 ).set_footer(text="Come back in 15 minutes to get another one!"),
                 view=MyView(),
                 ephemeral=True
            )
        
       
       
        me = await ctx.respond(
                embed=discord.Embed(
                     title="\🌐 | Checking your proxy...",
                     description=f"",
                     color=discord.Color.blue(),
                 ),
                 ephemeral=True,
            )  
        ppr = await check_proxy(proxy)
        await me.edit(embed=ppr)
        

    @commands.slash_command(name="proxy-stats", description="Shows stats about the number of proxies")
    async def show_stats(self, ctx: commands.Context):
        # Get the number of proxies in each type file
        tnum = 0
        pnum = []
        for proxy_type in proxy_types:
            with open(os.path.join(proxy_dir, f"{proxy_type.replace(' ', '-')}.txt")) as f:
                pnum.append(str(len(f.readlines())))
                
        for proxy_type in proxy_types:
            with open(os.path.join(proxy_dir, f"{proxy_type.replace(' ', '-')}.txt")) as f:
                tnum = tnum + len(f.readlines())
        # Create a formatted string with the stats
        stats_str = "## \🌐 | Proxy Stats"
        for i, proxy_type in enumerate(proxy_types):
            stats_str += f"\n* {proxy_type.capitalize()}: **{pnum[i]}**"
    
        # Create an embed object with the stats and send it in an ephemeral message
        embed = discord.Embed(
            title=" ",
            color=discord.Color.og_blurple(),
            description=f"### A significant amount of proxies have been wiped as they no longer work. \n"+stats_str + f"\n### Total: {tnum}",
        )
        await ctx.respond(embed=embed, ephemeral=True)
    @commands.Cog.listener()
    async def on_ready(self):
        
        await self.bot.wait_until_ready() # Wait until bot is ready
        await asyncio.sleep(1) 
        print("PROXYS: Resending panel message")
        guild = discord.utils.find(lambda g: g.id == 1101109470454632518, self.bot.guilds)
        channel = discord.utils.get(guild.channels, id=1116760627789181018)
        await channel.purge(limit=50, check=lambda message: message.author.id == 1116056397608656936)
        await channel.send(embed=discord.Embed(title="Proxy Dispenser",color=discord.Color.green(),description="Select one of the proxy types below to get one. 15 minute cooldown."), view=dispView())
async def check_proxy(url: str):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"http://{url}"
 
    try:
         response = await asyncio.wait_for(asyncio.to_thread(requests.get, url, timeout=10), timeout=15)
    except requests.Timeout:
         status = f"**\🟠 Timed out \n**This link may not work, you can try yourself if you want."
    except requests.RequestException:
         status = f"**\🔴 Invalid URL \n**This link may not work, you can try yourself if you want."
    else:
         if response.status_code >= 200 and response.status_code < 400:
             status = f"**\🟢 Working [HTTP {response.status_code}]** \nThis link works!"
         elif response.status_code == 403:
             status = f"**\🟡  Might Work [HTTP {response.status_code}]**\n### Rammerhead Proxies normally give HTTP 403."
         else:
             status = f"**\🔴 Not working [HTTP {response.status_code}]**\nThis link may not work, you can try yourself if you want."
 
    return discord.Embed(
         title=f"🌐 | I checked **{url}** for you!",
         description=f"This is what I got:\n### {status}",
         color=discord.Color.blue(),
     )


def setup(bot: commands.Bot):
    bot.add_cog(Proxys(bot))