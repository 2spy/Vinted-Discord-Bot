from pyVinted import Vinted
import discord
from discord.ext import tasks, commands
import asyncio
import json
import fade, os
from datetime import datetime
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta

with open("config.json", 'r') as config:
    confg = json.load(config)
cluster = MongoClient(confg["mangourl"])

textprint = """
██╗   ██╗██╗███╗   ██╗████████╗███████╗██████╗ 
██║   ██║██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
██║   ██║██║██╔██╗ ██║   ██║   █████╗  ██║  ██║
╚██╗ ██╔╝██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║
 ╚████╔╝ ██║██║ ╚████║   ██║   ███████╗██████╔╝
  ╚═══╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ 
         By 2$py#6495 > Premium Version
"""

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=">", intents=intents)
bot.remove_command("help")

os.system('cls')
fadedtext = fade.fire(textprint)
print(fadedtext)

db = cluster["client"]

vinted = Vinted("fr")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="By 2$py#6495 | My Prefix : >"))


def check_date_key(author_id):
    d1 = datetime.today().strftime('%d/%m/%Y').split("/")
    collection = db[str(author_id)]
    d2 = None
    for each_document in collection.find():
        if each_document["user"] == str(author_id):
            d2 = each_document["buydate"].split("/")
            break
    if datetime(int(d1[2]), int(d1[1]), int(d1[0])) >= datetime(int(d2[2]), int(d2[1]), int(d2[0])):
        return True
    else:
        return False


async def monitor_run(ctx, url):
    with open("monitor.json", 'r') as moniteur:
        monitor = json.load(moniteur)

    with open("monitor.json", "w+") as moniteur_txt:
        monitor[str(ctx.author.id)] = {}
        monitor[str(ctx.author.id)]["url"] = str(url)
        monitor[str(ctx.author.id)]["post"] = []
        json.dump(monitor, moniteur_txt, indent=4)
    await ctx.send(f"**{ctx.author.mention}** **> Le moniteur se lance dans 30 secondes !**")

    while True:
        await asyncio.sleep(30)
        with open("monitor.json", 'r') as moniteur:
            monitor = json.load(moniteur)
        vinted = Vinted("fr")
        if check_date_key(str(ctx.author.id)):
            await ctx.send(f"{ctx.author.mention} **> Votre abonnement est finit !**")
            return

        try:
            x = vinted.search(str(monitor[str(ctx.author.id)]["url"]), 5, 0)
            for post in x:
                with open('monitor.json', 'r') as populist:
                    allpost = json.load(populist)

                if post["id"] in allpost[str(ctx.author.id)]["post"] or post["country_id"] != 16:
                    continue
                else:
                    embed = discord.Embed(title="``👕``" + " " + post['title'], url=post['url'], color=0x09b7be,
                                          description=f"**Description :** ```YAML\n{post['description']}```")
                    embed.set_image(url=post["photos"][0]['url'])
                    embed.add_field(name="**💶 Prix**", value=f"**└**``{post['price']}``", inline=True)
                    embed.add_field(name="**📏 Taille**", value=f"**└**``{post['size']}``", inline=True)
                    embed.add_field(name="**🔖 Marque**", value=f"**└**``{post['brand']}``", inline=True)
                    embed.add_field(name="**📶 Dernière connexion du créateur du poste**",
                                    value=f"**└**``{post['user']['last_loged_on_ts'].replace('T', ' à ').replace('+01:00', '')}``",
                                    inline=True)
                    embed.add_field(name="**👍 Avis positif**",
                                    value=f"**└**``{post['user']['positive_feedback_count']}``", inline=True)
                    embed.add_field(name="**👎 Avis négatif**",
                                    value=f"**└**``{post['user']['negative_feedback_count']}``", inline=True)
                    embed.set_footer(
                        text=f"✉ Posté le : {post['created_at_ts'].replace('T', ' à ').replace('+01:00', '')} | By 2$py#6495")

                    with open("monitor.json", 'w+') as moniteur:
                        monitor[str(ctx.author.id)]["post"].append(post['id'])
                        json.dump(monitor, moniteur, indent=4)
                    await ctx.send(embed=embed)
        except:
            await asyncio.sleep(30)
            pass


@bot.command()
async def changeurl(ctx, url):
    with open("monitor.json", 'r') as moniteur:
        monitorjson = json.load(moniteur)

    with open("monitor.json", "w+") as moniteur:
        monitorjson[str(ctx.author.id)]["url"] = str(url)
        json.dump(monitorjson, moniteur, indent=4)
    await ctx.send(f"{ctx.author.mention} **> Lien changé !**")


@bot.command()
async def valide(ctx, key):
    date_after_month = datetime.today() + relativedelta(months=1)
    temp = date_after_month.strftime('%d/%m/%Y')
    with open("keylist.txt", 'r') as f:
        content = f.read()
        content_list = content.splitlines()
        if key not in content_list:
            await ctx.send(f"{ctx.author.mention} **> Clé a été déjà activé  !**")
            return

    logskey = bot.get_channel(939807147347296307)
    collection = db[str(ctx.author.id)]
    new_values = {'user': str(ctx.author.id), "buydate": str(temp), "key": str(key)}
    collection.insert_one(new_values)
    await ctx.send(
        f"✏ **> Clé lié à {ctx.author.name}**\n🕐 **Date d'activation :** {str(datetime.today().strftime('%d/%m/%Y'))}\n🕐 **Date d'expiration :** {str(date_after_month.strftime('%d/%m/%Y'))}")
    await logskey.send(
        f"✏ **> Clé lié à <@{ctx.author.id}>**\n🕐 **Date d'activation :** {str(datetime.today().strftime('%d/%m/%Y'))}\n🕐 **Date d'expiration :** {str(date_after_month.strftime('%d/%m/%Y'))}")

    try:
        with open('keylist.txt', 'r') as fr:
            lines = fr.readlines()

            with open('keylist.txt', 'w') as fw:
                for line in lines:
                    if line.strip('\n') != str(key):
                        fw.write(line)
    except:
        pass


@bot.command()
async def mymonitor(ctx, url):
    bot.loop.create_task(monitor_run(ctx, url))


bot.run(confg["discordbottoken"])
