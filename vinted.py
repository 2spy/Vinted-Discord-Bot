import os
import shutil
import json, asyncio
try:
    import requests
    from bs4 import BeautifulSoup
    import discord
    import fade
    from discord_slash import ButtonStyle, SlashCommand
    from discord_slash.utils.manage_components import *
    from discord.ext import commands
except:
    os.system("pip install requests")
    os.system("pip install discord")
    os.system("pip install fade")
    os.system("pip install bs4")
    os.system("pip install discord-py-slash-command ")


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
        str(url))
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
    pays = userinfo["user"]["country_title"]
    ville = userinfo["user"]["city"]

    lesinfo = {}
    lesinfo["titre"] = titre
    lesinfo["description"] = description
    lesinfo["buybutton"] = buybutton
    lesinfo["positive"] = positive
    lesinfo["negative"] = negative
    lesinfo["username"] = username
    lesinfo["pays"] = pays
    lesinfo["ville"] = ville
    return lesinfo


def search(url):
    reponse = requests.get(str(url))
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

with open("config.json", 'r') as config:
    configs = json.load(config)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=configs["prefix"], intents=intents)
bot.remove_command("help")

os.system('cls')
slash = SlashCommand(bot, SlashCommand)


@bot.event
async def on_ready():
    fadedtext = r"""
                                ██╗   ██╗██╗███╗   ██╗████████╗███████╗██████╗ 
                                ██║   ██║██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
                                ██║   ██║██║██╔██╗ ██║   ██║   █████╗  ██║  ██║
                                ╚██╗ ██╔╝██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║
                                 ╚████╔╝ ██║██║ ╚████║   ██║   ███████╗██████╔╝
                                  ╚═══╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ 
                                                  By 2$py#6495"""
    faded = fade.water(fadedtext)
    print(str(faded).center(shutil.get_terminal_size().columns))
    print(f"    {Spy.bleu}${Spy.blanc} System : {Spy.bleu}Welcome in Vinted Bot :) !")
    print(f"    {Spy.bleu}${Spy.blanc} System > {Spy.bleu}I'm connected to {bot.user.name} !")
    print(f"    {Spy.bleu}${Spy.blanc} System > {Spy.bleu}My prefix is '{configs['prefix']}' !")
    await bot.change_presence(activity=discord.Game(name=configs["status"]))


posting = []


async def moniteur(channelid, url):
    channel = bot.get_channel(channelid)
    while True:
        try:
            z = search(str(url))
        except Exception as err:
            print(err)
            pass

        try:
            x = z["items"]["catalogItems"]["byId"]
            dictlist = list(x)
            for i in range(7, -1, -1):
                try:
                    post = dictlist[i]

                    try:
                        info = get_info_post(x[str(post)]["url"])
                    except Exception as err:
                        continue

                    if post in posting:
                        continue
                    else:
                        embed = discord.Embed(title="``👕``" + " " + x[post]['title'],
                                              description=f"```fix\n{info['description']}```", url=x[post]['url'],
                                              color=0x09b7be)
                        embed.add_field(name="**``💶`` Prix**", value=f"```yaml\n{x[post]['price']}€```", inline=True)
                        embed.add_field(name="**``📏`` Taille**", value=f"```yaml\n{x[post]['size_title']}```",
                                        inline=True)
                        embed.add_field(name="**``🔖`` Marque**", value=f"```yaml\n{x[post]['brand_title']}```",
                                        inline=True)
                        embed.add_field(name="**``👍`` Avis positif**", value=f"```yaml\n{str(info['positive'])}```",
                                        inline=True)
                        embed.add_field(name="**``👎`` Avis négatif**", value=f"```yaml\n{str(info['negative'])}```",
                                        inline=True)
                        embed.add_field(name="**``📍`` Emplacement :**",
                                        value=f"```yaml\n{info['pays']}, {info['ville']}```", inline=True)
                        embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                        embed.set_footer(text=f"つ ◕_◕ ༽つ Posté par : {info['username']}")
                        buttons = [
                            create_button(style=ButtonStyle.URL, emoji="🛒", label="Acheter",
                                          url=str(info["buybutton"])),
                            create_button(style=ButtonStyle.URL, emoji="🔎", label="Détails",
                                          url=str(x[str(post)]["url"])),
                        ]
                        action_row = create_actionrow(*buttons)
                        await channel.send(embed=embed, components=[action_row])
                        posting.append(post)
                except:
                    pass
            await asyncio.sleep(5)

        except:
            pass



@bot.command()
async def sub(ctx, url):
    if url in configs["suburl"]:
        pass
    else:
        with open("config.json", 'w+') as config:
            configs["suburl"][str(url)] = {}
            configs["suburl"][str(url)]["channel"] = ctx.channel.id
            json.dump(configs, config, indent=4)

    task = asyncio.create_task(moniteur(ctx.channel.id, url))
    embed = discord.Embed(title="❤ **__Merci d'utiliser le bot !__**",
                          description="Vous utilisez la version 2 du bot !",
                          color=0x09b7be)
    embed.add_field(name="La recherche en cours :", value=f"```yaml\n{url}```")
    embed.add_field(name="Nom de la tâche :",
                    value=f"```yaml\n{task.get_name()}```")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/939851736863105074/9a317142e664084d54c48a18ff46de40.webp?size=1024")
    embed.set_footer(text="つ ◕_◕ ༽つ Dev by 2$py#6495")
    await ctx.send(embed=embed)
    await task


@bot.command()
async def run(ctx):
    task = ""
    for suburl in configs["suburl"]:
        if ctx.channel.id == configs["suburl"][str(suburl)]["channel"]:
            task = asyncio.create_task(moniteur(ctx.channel.id, suburl))
            embed = discord.Embed(title="❤ **__Merci d'utiliser le bot !__**",
                                  description="```yaml\nVous utilisez la version 2 du bot !```",
                                  color=0x09b7be)
            embed.add_field(name="Lancement de la tache associé au salon :",
                            value=f"```yaml\n{suburl}```")
            embed.add_field(name="Nom de la tâche :",
                            value=f"```yaml\n{task.get_name()}```")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/939851736863105074/9a317142e664084d54c48a18ff46de40.webp?size=1024")
            embed.set_footer(text="つ ◕_◕ ༽つ Dev by 2$py#6495")
            await ctx.send(embed=embed)
            await task
            break
    await ctx.send(f"{ctx.author.mention} **- Aucun lien n'est affilié à ce salon !**")



@bot.command()
async def stop(ctx, name):
    pending = asyncio.all_tasks()
    for ele in pending:
        if ele.get_name() == name:
            ele.cancel()
            await ctx.send(f"{ctx.author.mention} - **La tâche a été stoppé !**")
            return
    await ctx.send(f"{ctx.author.mention} - **Aucune tâche trouvé !**")


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🤖 **__Bienvenue dans le menu d'aide du bot__**",
                          description="Version actuelle du bot 2.0", color=0x09b7be)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/939851736863105074/9a317142e664084d54c48a18ff46de40.webp?size=1024")
    embed.add_field(name="$help", value="```yaml\nOuvre le menu d'aide du bot```", inline=False)
    embed.add_field(name="$sub", value="```yaml\nLance le bot en fonction de l'url```", inline=False)
    embed.add_field(name="$stop", value="```yaml\nEcrivez juste $stop nom_de_la_tache et le bot stoppera la tâche!```", inline=False)
    embed.add_field(name="$run", value="```yaml\nRelance la tâche associé au salon sans reécrire la commande $sub```", inline=False)
    embed.add_field(name="$ping", value="```yaml\nAffiche le ping du bot !```", inline=False)
    embed.set_footer(text="つ ◕_◕ ༽つ Dev by 2$py#6495")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention} **- Latence du bot :** ``{round(bot.latency * 1000)} ms`` 🚀')


bot.run(configs["token"])
