from ressources import get_config
from ressources.core.configure import msg_prefix, change_prefix as sys_change_prefix, update_google_reactions_wrapper
from ressources.core.configure_roles import add_admin_role, remove_admin_role
from ressources.core.configure_permissions import ban, unban
from discord import Embed, Role, Member, Emoji
from . import client, get_prefix


@client.command()
async def deny(ctx, member: Member):
    await ban(ctx.message, member)


@client.command()
async def allow(ctx, member: Member):
    await unban(ctx.message, member)


@client.command()
async def prefix(ctx):
    await msg_prefix(ctx.message)


@client.command()
async def change_prefix(ctx, new_prefix: str):
    await sys_change_prefix(ctx.message, new_prefix)

@client.command()
async def change_google_reaction(ctx, emoji: Emoji):
    await update_google_reactions_wrapper(ctx.message, emoji)

@client.command()
async def add_role(ctx, role: Role):
    await add_admin_role(ctx.message, role)

@client.command()
async def remove_role(ctx, role: Role):
    await remove_admin_role(ctx.message, role)


@client.command()
async def help(ctx):
    embed = Embed()

    embed.set_author(
        name="AdriBloober#9372 & TNT2k#7587",
        icon_url="https://pbs.twimg.com/profile_images/843734935022256129/-2pD4h7u_400x400.jpg",
    )
    embed.set_footer(text="OpenSource project")

    commands = [
        {"name": f"{await get_prefix(None, ctx.message)}help", "value": "Hilfe anzeigen"},
        {"name": f"{await get_prefix(None, ctx.message)}prefix", "value": "Präfix anzeigen"},
        {"name": f"{await get_prefix(None, ctx.message)}change_prefix <prefix>", "value": "Prefix ändern"},
        {"name": f"{await get_prefix(None, ctx.message)}deny <@User>", "value": "Nutzer für Google Anfragen sperren"},
        {"name": f"{await get_prefix(None, ctx.message)}allow <@User>",
         "value": "Nutzer für Google Anfragen entsperren"},
    ]

    for command in commands:
        embed.add_field(name=command["name"], value=command["value"], inline=False)

    embed.add_field(name="CX Types", value="Mit diesen Commands kannst du googlen: ")

    for cx_type in get_config().ctx_types:
        embed.add_field(
            name=f"{cx_type}: <search_query>", value=f"Auf {cx_type} suchen", inline=False
        )

    await ctx.send(embed=embed)
