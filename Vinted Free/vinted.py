from pyVinted import Vinted
import discord
from discord.ext import tasks, commands
import asyncio
import json
import fade, os
from pymongo import MongoClient
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
           By 2$py#6495 > Free Version
"""

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

os.system('cls')
fadedtext = fade.fire(textprint)
print(fadedtext)

with open("marqueid.json", 'r') as marque:
    brand = json.load(marque)

with open("marqueid.json", 'r') as marque:
    brand = json.load(marque)
db = cluster["client"]

vinted = Vinted("fr")
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="My Prefix : !"))

@tasks.loop(minutes=2)
async def botrun():
    vinted = Vinted("fr")
    for ele in brand['marque']:
        try:
            ids = brand[ele]["id"]
            saloni = bot.get_channel(brand[ele]['salonid'])

            x = vinted.search(
                f"https://www.vinted.fr/vetements?brand_id[]={ids}&order=newest_first&price_to=120&currency=EUR", 5, 0)
            for post in x:
                with open('vintedpost.json', 'r') as populist:
                    allpost = json.load(populist)

                if post['id'] in allpost['post'] or post["country_id"] != 16 or post["size_id"] in [1230, 311, 1228,
                                                                                                    1226,
                                                                                                    102, 310, 1229,
                                                                                                    1227, 312]:
                    continue
                else:
                    embed = discord.Embed(title="``👕``" + " " + post['title'], url=post['url'], color=0x00FF00,
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

                    with open("vintedpost.json", 'w+') as fishier:
                        allpost["post"].append(post['id'])
                        json.dump(allpost, fishier, indent=4)
                    await saloni.send(embed=embed)
        except:
            await asyncio.sleep(2)
            pass

@bot.command()
async def run(ctx):
    botrun.start()


bot.run(confg["discordbottoken"])