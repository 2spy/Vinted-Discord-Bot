import os
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks, commands
import json, asyncio
import fade


def search(url):
    reponse = requests.get(str(url), timeout=1)
    print(reponse)
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
bot = commands.Bot(command_prefix=">", intents=intents)
bot.remove_command("help")

os.system('cls')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="My Prefix : !"))

posting = []
@tasks.loop(seconds=0)
async def nike(limit):
    try:
        z = search(
            "https://www.vinted.fr/vetements?z_id[]=53&order=newest_first&size_id[]=207&size_id[]=208&size_id[]=209&size_id[]=210&size_id[]=211&brand_id[]=53")
    except:
        nike.restart(limit=5)
    count = 0
    saloni = bot.get_channel(941043958690218044)
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            if count == limit:
                break
            if post in posting:
                pass
            else:
                print(x[post])
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'], url=x[post]['url'], color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Nombre de vue du poste : {x[post]['view_count']}")

                await saloni.send(embed=embed)
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)



@tasks.loop(seconds=0)
async def lacoste(limit):
    try:
        z = search(
            "https://www.vinted.fr/vetements?z_id[]=53&order=newest_first&size_id[]=207&size_id[]=208&size_id[]=209&size_id[]=210&size_id[]=211&brand_id[]=304")
    except:
        nike.restart(limit=5)
    count = 0
    saloni = bot.get_channel(941043999869915166)
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            if count == limit:
                break
            if post in posting:
                pass
            else:
                print(x[post])
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'], url=x[post]['url'], color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Nombre de vue du poste : {x[post]['view_count']}")

                await saloni.send(embed=embed)
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)

@tasks.loop(seconds=0)
async def adidas(limit):
    try:
        z = search(
            "https://www.vinted.fr/vetements?z_id[]=53&order=newest_first&size_id[]=207&size_id[]=208&size_id[]=209&size_id[]=210&size_id[]=211&brand_id[]=14")
    except:
        nike.restart(limit=5)
    count = 0
    saloni = bot.get_channel(941044039585771530)
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            if count == limit:
                break
            if post in posting:
                pass
            else:
                print(x[post])
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'], url=x[post]['url'], color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Nombre de vue du poste : {x[post]['view_count']}")

                await saloni.send(embed=embed)
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)

@tasks.loop(seconds=0)
async def ralph(limit):
    try:
        z = search(
            "https://www.vinted.fr/vetements?z_id[]=53&order=newest_first&size_id[]=207&size_id[]=208&size_id[]=209&size_id[]=210&size_id[]=211&brand_id[]=88")
    except:
        nike.restart(limit=5)
    count = 0
    saloni = bot.get_channel(941044080278917140)
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            if count == limit:
                break
            if post in posting:
                pass
            else:
                print(x[post])
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'], url=x[post]['url'], color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Nombre de vue du poste : {x[post]['view_count']}")

                await saloni.send(embed=embed)
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)

@tasks.loop(seconds=0)
async def carhart(limit):
    try:
        z = search(
            "https://www.vinted.fr/vetements?z_id[]=53&order=newest_first&size_id[]=207&size_id[]=208&size_id[]=209&size_id[]=210&size_id[]=211&brand_id[]=362")
    except:
        nike.restart(limit=5)
    count = 0
    saloni = bot.get_channel(941044164714438687)
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            if count == limit:
                break
            if post in posting:
                pass
            else:
                print(x[post])
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'], url=x[post]['url'], color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Nombre de vue du poste : {x[post]['view_count']}")

                await saloni.send(embed=embed)
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)

@tasks.loop(seconds=0)
async def carhart(limit):
    try:
        z = search(
            "https://www.vinted.fr/vetements?z_id[]=53&order=newest_first&size_id[]=207&size_id[]=208&size_id[]=209&size_id[]=210&size_id[]=211&brand_id[]=362")
    except:
        nike.restart(limit=5)
    count = 0
    saloni = bot.get_channel(941044164714438687)
    try:
        x = z["items"]["catalogItems"]["byId"]
        for post in x:
            if count == limit:
                break
            if post in posting:
                pass
            else:
                print(x[post])
                embed = discord.Embed(title="``👕``" + " " + x[post]['title'], url=x[post]['url'], color=0x09b7be)
                embed.add_field(name="**💶 Prix**", value=f"**└**``{x[post]['price']}€``", inline=True)
                embed.add_field(name="**📏 Taille**", value=f"**└**``{x[post]['size_title']}``", inline=True)
                embed.add_field(name="**🔖 Marque**", value=f"**└**``{x[post]['brand_title']}``", inline=True)
                embed.set_image(url=x[post]["photo"]["thumbnails"][4]["url"])
                embed.set_footer(text=f"👁️ Nombre de vue du poste : {x[post]['view_count']}")

                await saloni.send(embed=embed)
                posting.append(post)
            count += 1
            await asyncio.sleep(3)

    except:
        await asyncio.sleep(2)

@bot.command()
async def run(ctx, limit=2):
    await ctx.send("Le bot est lancé !")
    nike.start(limit)
    lacoste.start(limit)
    adidas.start(limit)
    ralph.start(limit)
    carhart.start(limit)


bot.run("OTM5ODUxNzM2ODYzMTA1MDc0.Yf-3Iw.baFZntKTCV30kdSSHO1i6oUdVmo")
