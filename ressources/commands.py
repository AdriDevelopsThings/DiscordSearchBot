from ressources import get_config, get_prefix
from .permissions import ban, unban, prefix, change_prefix
from discord import Embed
from . import client


@client.command()
async def deny(ctx):
    await ban(ctx.message)


@client.command()
async def allow(ctx):
    await unban(ctx.message)


@client.command()
async def prefix(ctx):
    await prefix(ctx.message)


@client.command()
async def change_prefix(ctx):
    await change_prefix(ctx.message)


@client.command()
async def help(ctx):
    embed = Embed()

    embed.set_author(
        name="AdriBloober#9372 & TNT2k#7587",
        icon_url="https://pbs.twimg.com/profile_images/843734935022256129/-2pD4h7u_400x400.jpg",
    )
    embed.set_footer(text="OpenSource project")

    commands = [
        {"name": f"{get_prefix(None, ctx.message)}help", "value": "Hilfe anzeigen"},
        {"name": f"{get_prefix(None, ctx.message)}prefix", "value": "Prefix anzeigen"},
        {"name": f"{get_prefix(None, ctx.message)}change_prefix <prefix>", "value": "Prefix ändern"},
        {"name": f"{get_prefix(None, ctx.message)}allow <@User>", "value": "Nutzer für Google Anfragen sperren"},
        {"name": f"{get_prefix(None, ctx.message)}deny <@User>", "value": "Nutzer für Google Anfragen entsperren"},
    ]

    for command in commands:
        embed.add_field(name=command["name"], value=command["value"], inline=False)

    embed.add_field(name="CX Types", value="Mit diesen Commands kannst du googlen: ")

    for cx_type in get_config().ctx_types:
        embed.add_field(
            name=f"{cx_type}: <search_query>", value=f"Auf {cx_type} googlen", inline=False
        )

    await ctx.send(embed=embed)
