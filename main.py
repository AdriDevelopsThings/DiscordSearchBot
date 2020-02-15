import discord
from discord.ext import commands

import settings
from core.api import Api
from urllib.parse import quote
from core import j

def is_permited_to_ban(guild, member):
    if member.id == 330148908531580928:
        return True
    team_role = guild.get_role(427495972973838358)
    return team_role in member.roles
bot = commands.Bot(command_prefix="§")
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

        json = j.read()
        if message.author.id in json:
            await message.add_reaction("❌")
            return

        content = message.content.replace("google: ", "")
        s = api.search(content)
        if s is None:
            await message.channel.send("0 Ergebnisse gefunden")
        else:
            embed = discord.Embed(title="Google suche", description=content)
            for value in s:
                embed.add_field(name=value["title"], value=value["link"], inline=False)
            embed.set_footer(text=f"Angefragt von {str(message.author)}")
            await message.channel.send(embed=embed)
    elif message.content.startswith("lmgtfy: "):
        content = message.content.replace("lmgtfy: ", "")
        content = quote(content)
        content = content.replace("%20", "+")
        link = "https://lmgtfy.com/?q=" + content
        await message.channel.send(link)
    elif message.content.startswith("§ban "):
        json = j.read()
        user = message.content.replace("§ban ", "").replace("<", "").replace(">", "").replace("@", "").replace("!", "")
        try:
            user = bot.get_user(int(user))
            if user is None:
                raise ValueError
        except ValueError:
            await message.channel.send("Der Nutzer existiert nicht oder das Kommando ist falsch aufgebaut!")
            return
        if user.id in json:
            await message.channel.send("Der Nutzer ist bereits gebannt!")
        else:
            if not is_permited_to_ban(message.guild, message.author):
                await message.add_reaction("❌")
                return
            json.append(user.id)
            j.write(json)
            await message.channel.send(
                f"Der Nutzer {user} wurde erfolgreich gebannt!"
            )
    elif message.content.startswith("§unban "):
        json = j.read()
        user = message.content.replace("§unban ", "").replace("<","").replace(">", "").replace("@", "").replace("!", "")
        try:
            user = bot.get_user(int(user))
            if user is None:
                raise ValueError
        except ValueError:
            await message.channel.send("Der Nutzer existiert nicht oder das Kommando ist falsch aufgebaut!")
            return
        if not user.id in json:
            await message.channel.send("Der Nutzer ist nicht gebannt!")
        else:
            if not is_permited_to_ban(message.guild, message.author):
                await message.add_reaction("❌")
                return
            json.remove(user.id)
            j.write(json)
            await message.channel.send(
                f"Der Nutzer {user} wurde entbannt!"
            )


invalid = []



@bot.event
async def on_reaction_add(reaction, user):
    json = j.read()
    if user.id in json:
        return
    if reaction.count != 1 or reaction.message.id in invalid:
        return
    if (
        str(reaction) == "❌"
        and is_permited_to_ban(reaction.message.guild, user)
        and reaction.message.content.startswith("google: ")
    ):
        json.append(reaction.message.author.id)
        j.write(json)
        await reaction.message.channel.send(
            f"Der Nutzer {reaction.message.author} wurde erfolgreich gebannt!"
        )

    if (
        str(reaction) == "<:google:331075369501196290>"
        or str(reaction) == "<:google:677939519160451093>"
    ):
        content = reaction.message.content
        s = api.search(content)
        invalid.append(reaction.message.id)
        if s is None:
            await reaction.message.channel.send("0 Ergebnisse gefunden")
        else:
            embed = discord.Embed(title="Google suche", description=content)
            for value in s:
                embed.add_field(name=value["title"], value=value["link"], inline=False)
                embed.set_footer(text=f"Angefragt von {str(user)}")
            await reaction.message.channel.send(embed=embed)

bot.run(settings.DISCORD_BOT_TOKEN.get_string())
