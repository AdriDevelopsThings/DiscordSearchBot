import discord
from discord.ext import commands

import settings
from core.api import Api
from urllib.parse import quote


bot = commands.Bot(command_prefix="$")
bot.remove_command("help")
api = Api()


@bot.event
async def on_ready():
    print("Ready")
    activity = discord.Activity(name="Geil")
    await bot.change_presence(activity=activity, status=discord.Status.idle)
    api.ini()


@bot.event
async def on_message(message):
    if message.content.startswith("google: "):

        content = message.content.replace("google: ", "")
        s = api.search(content)
        if s is None:
            await message.channel.send("0 Ergebnisse gefunden")
        else:
            embed = discord.Embed(title="Google suche", description=content)
            for value in s:
                embed.add_field(name=value["title"], value=value["link"], inline=False)
            await message.channel.send(embed=embed)
    elif message.content.startswith("lmgtfy: "):
        content = message.content.replace("lmgtfy: ", "")
        content = quote(content)
        content = content.replace("%20", "+")
        link = "https://lmgtfy.com/?q=" + content
        await message.channel.send(link)

invalid = []

@bot.event
async def on_reaction_add(reaction, user):#
    if reaction.count != 1 or reaction.message.id in invalid:
        return
    if str(reaction) == "<:google:331075369501196290>" or str(reaction) == "<:google:677939519160451093>":
        content = reaction.message.content
        s = api.search(content)
        invalid.append(reaction.message.id)
        if s is None:
            await reaction.message.channel.send("0 Ergebnisse gefunden")
        else:
            embed = discord.Embed(title="Google suche", description=content)
            for value in s:
                embed.add_field(name=value["title"], value=value["link"], inline=False)
            await reaction.message.channel.send(embed=embed)


bot.run(settings.DISCORD_BOT_TOKEN.get_string())
