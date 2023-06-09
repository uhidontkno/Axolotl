# Axolotl
 A multi-purpose bot including moderation, fun, utility, proxies, etc. 

# Installation
Run `pip install pillow numpy re py-cord discord.py asyncio`, if I miss any, just install them if there is a ModuleNotFound error.

# How to setup:
You need a `token.env` file containing **ONLY** your discord bot's token, 
in order to use the Proxies feature you need a folder called `proxies` with a textfile containing each type of proxy, seperated by a new line.
Then to add or remove a proxy type, go into `proxys.py` and change the `proxy_types` table with each type of proxy. For Example:
```py
proxy_types = [
          "artclass",
          "emerald",
          "holy-unblocker",
          "hypertabs"
        ]
```
Also change array p_c with the Discord of each proxy type, if you don't know put `N/A`.

Then, just run `py main.py`