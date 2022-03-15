import discord
from discord.ext import commands
import os, json


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command("help")

os.system('cls')

with open("config.json", 'r') as config:
    configs = json.load(config)

@bot.event
async def on_ready():
    print("Connecté chef !")
    await bot.change_presence(activity=discord.Game(name="2$py le boss !"))

@bot.command()
async def sub(ctx, vintedurl):
    x = await ctx.channel.create_webhook(name="Discord-test")
    with open("config.json", 'w+') as configedit:
        configs["suburl"][str(x.url)] = {}
        configs["suburl"][str(x.url)]["url"] = str(vintedurl)
        configs["suburl"][str(x.url)]["salon"] = str(ctx.channel.name)

        json.dump(configs,configedit,indent=4)
    await ctx.send("Webhook ajouté avec le lien !")
bot.run(configs["token"])