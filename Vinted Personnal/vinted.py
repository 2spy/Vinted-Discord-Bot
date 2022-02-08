from pyVinted import Vinted
import discord
from discord.ext import tasks, commands
import asyncio
import json
import fade, os

with open("config.json", 'r') as config:
    confg = json.load(config)

textprint = """
██╗   ██╗██╗███╗   ██╗████████╗███████╗██████╗ 
██║   ██║██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
██║   ██║██║██╔██╗ ██║   ██║   █████╗  ██║  ██║
╚██╗ ██╔╝██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║
 ╚████╔╝ ██║██║ ╚████║   ██║   ███████╗██████╔╝
  ╚═══╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ 
         By 2$py#6495 > Personal Version
"""

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

os.system('cls')
fadedtext = fade.fire(textprint)
print(fadedtext)

vinted = Vinted("fr")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="My Prefix : !"))


async def botrun(ctx, url):
    vinted = Vinted("fr")
    while True:
        try:
            x = vinted.search(url, 5, 0)
            for post in x:
                with open('vintedpost.json', 'r') as populist:
                    allpost = json.load(populist)

                if post['id'] in allpost['post'] or post["country_id"] != 16:
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

                    with open("vintedpost.json", 'w+') as fishier:
                        allpost["post"].append(post['id'])
                        json.dump(allpost, fishier, indent=4)
                    await ctx.send(embed=embed)
        except:
            vinted = Vinted("fr")
            await asyncio.sleep(30)
            pass


@bot.command()
async def run(ctx, url):
    bot.loop.create_task(botrun(ctx, url))


bot.run(confg["discordbottoken"])
