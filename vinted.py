import os
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks, commands
import json, asyncio
import fade
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
from discord.ext import commands


class Spy:
    gris = "\033[1;30;1m"
    rouge = "\033[1;31;1m"
    vert = "\033[1;32;1m"
    jaune = "\033[1;33;1m"
    bleu = "\033[1;34;1m"
    violet = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    blanc = "\033[2;0;1m"


def get_info_post(url):
    reponse = requests.get(
        str(url),
        timeout=5)
    soup = BeautifulSoup(reponse.text, "html.parser")

    res = soup.findAll('script', {"class": "js-react-on-rails-component"})

    description = json.loads(res[15].text.replace(
        '<script class="js-react-on-rails-component" data-component-name="ItemDescription" data-dom-id="ItemDescription-react-component-3d79657d-a1b5-4f1d-b501-2f470f328c66" type="application/json">',
        "").replace("</script>", ''))
    buybutton = json.loads(res[17].text.replace(
        '<script class="js-react-on-rails-component" data-component-name="ItemBuyButton" data-dom-id="ItemBuyButton-react-component-026520bb-78fd-4e8f-9477-541dcafab42d" type="application/json">',
        "").replace("</script>", ''))
    userinfo = json.loads(res[19].text.replace(
        '<script class="js-react-on-rails-component" data-component-name="ItemUserInfo" data-dom-id="ItemUserInfo-react-component-2105d904-b161-47d1-bfce-9b897a8c1cc6" type="application/json">',
        '').replace("</script>", ''))

    titre = description["content"]["title"]
    description = description["content"]["description"]
    buybutton = "https://www.vinted.fr" + buybutton["path"]
    positive = userinfo["user"]["positive_feedback_count"]
    negative = userinfo["user"]["negative_feedback_count"]
    username = userinfo["user"]["login"]

    lesinfo = {}
    lesinfo["titre"] = titre
    lesinfo["description"] = description
    lesinfo["buybutton"] = buybutton
    lesinfo["positive"] = positive
    lesinfo["negative"] = negative
    lesinfo["username"] = username
    return lesinfo


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
slash = SlashCommand(bot, SlashCommand)

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


@tasks.loop(seconds=15)
async def moniteur(ctx, url, limit):
    url2 = url
    ctx2 = ctx
    try:
        z = search(str(url))
    except:
        moniteur.restart(ctx, url2, limit=8)
    count = 0
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            info = get_info_post(x[str(post)]["url"])
            if count == limit:
                break
            if post in posting:
                pass
            else:
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'],
                                      description=f"```fix\n{info['description']}```", url=x[post]['url'],
                                      color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.add_field(name="**👍 Avis positif**", value=f"**└**``{str(info['positive'])}``", inline=True)
                embed.add_field(name="**👎 Avis négatif**", value=f"**└**``{str(info['negative'])}``", inline=True)
                embed.add_field(name="**🦾 Soon**", value=f"ㅤ", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Posté par : {info['username']}")
                buttons = [
                    create_button(style=ButtonStyle.URL, emoji="🛒",label="Acheter",url=str(info["buybutton"])),
                ]
                action_row = create_actionrow(*buttons)
                msg = await ctx.send(embed=embed, components=[action_row])
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)


@bot.command()
async def sub(ctx, url, limit=8):
    embed = discord.Embed(title="**__Merci d'utiliser le bot !__**",description="Vous utilisez la version 2 du bot !",color=0x09b7be)
    embed.add_field(name="La recherche en cours :",value=f"```fix\n{url}```")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/939851736863105074/9a317142e664084d54c48a18ff46de40.webp?size=1024")
    embed.add_field(name="Nomre de poste :",value=f"```fix\n{limit}```")
    embed.set_footer(text="Dev by 2$py#6495")
    await ctx.send(embed=embed)
    moniteur.start(ctx, url, limit)

@bot.command()
async def stop(ctx):
    if moniteur.is_running():
        await ctx.send(f"{ctx.author.mention} - **Le bot a été stoppé !**")
        moniteur.stop()
    else:
        await ctx.send(f"{ctx.author.mention} - **Le bot n'est pas lancé !**")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**__Bienvenue dans le menu d'aide du bot__**",description="Version actuelle du bot 2.0",color=0x09b7be)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/939851736863105074/9a317142e664084d54c48a18ff46de40.webp?size=1024")
    embed.add_field(name="$help",value="```fix\nOuvre le menu d'aide du bot```", inline=False)
    embed.add_field(name="$sub",value="```fix\nLance le bot en fonction de l'url et de la limite```",inline=False)
    embed.add_field(name="$stop",value="```fix\nEcrivez juste $stop et le bot s'arretera !```",inline=False)
    embed.set_footer(text="Bot développé par : 2$py#6495")
    await ctx.send(embed=embed)

with open("config.json", 'r') as config:
    configs = json.load(config)
bot.run(configs["token"])
