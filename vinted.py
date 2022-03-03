import os
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks, commands
import json, asyncio
import fade

class Spy:
    gris = "\033[1;30;1m"
    rouge = "\033[1;31;1m"
    vert = "\033[1;32;1m"
    jaune = "\033[1;33;1m"
    bleu = "\033[1;34;1m"
    violet = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    blanc = "\033[2;0;1m"

def search(url):
    reponse = requests.get(str(url), timeout=1)
    soup = BeautifulSoup(reponse.text, "html.parser")

    res = soup.findAll('script')
    value = res[48].text.replace('<script z-js-react-on-rails-store="MainStore" type="application/json">', "")
    z = json.loads(value)

    del z["intl"]
    del z["session"]
    del z["screen"]
    del z["abTests"]
    del z["auth"]
    del z["savedSearches"]
    del z["ads"]
    del z["catalogFilters"]
    del z["items"]["catalogItems"]["ids"]
    return z


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command("help")

os.system('cls')


@bot.event
async def on_ready():
    fadedtext = r"""
                             ______
                            /     /\
                           /     /##\
                          /     /####\
                         /     /######\
                        /     /########\
                       /     /##########\
                      /     /#####/\#####\
                     /     /#####/++\#####\
                    /     /#####/++++\#####\
                   /     /#####/\+++++\#####\
                  /     /#####/  \+++++\#####\
                 /     /#####/    \+++++\#####\
                /     /#####/      \+++++\#####\
                        ███████╗██████╗ ██╗   ██╗
                        ██╔════╝██╔══██╗╚██╗ ██╔╝
                        ███████╗██████╔╝ ╚████╔╝ 
                        ╚════██║██╔═══╝   ╚██╔╝  
                        ███████║██║        ██║   
                        ╚══════╝╚═╝        ╚═╝   
           /     /#####/        \+++++\#####\
          /     /#####/__________\+++++\#####\
         /                        \+++++\#####\
        /__________________________\+++++\####/
        \+++++++++++++++++++++++++++++++++\##/
         \+++++++++++++++++++++++++++++++++\/
          ``````````````````````````````````
    """
    faded = fade.blackwhite(fadedtext)
    print(faded)
    print(f"    {Spy.bleu}${Spy.blanc} System : {Spy.bleu}Welcome in Vinted Bot :) !")
    print(f"    {Spy.bleu}${Spy.blanc} System > {Spy.bleu}I'm connected to {bot.user.name} !")
    print(f"    {Spy.bleu}${Spy.blanc} System > {Spy.bleu}My prefix is '$' !")
    await bot.change_presence(activity=discord.Game(name="My Prefix : $"))

posting = []
@tasks.loop(seconds=0)
async def moniteur(url, limit, ctx):
    try:
        z = search(str(url))
    except:
        moniteur.restart(limit=5)
    count = 0
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            if count == limit:
                break
            if post in posting:
                pass
            else:
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'], url=x[post]['url'], color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Nombre de vue du poste : {x[post]['view_count']}")

                await ctx.send(embed=embed)
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)




@bot.command()
async def sub(ctx,url, limit=2):
    await ctx.send("Le bot est lancé !")
    await bot.loop.create_task(moniteur(url,limit,ctx))


with open("config.json", 'r') as config:
    configs = json.load(config)
bot.run(configs["token"])
