from resources import get_config
from resources.core.configure import (
    msg_prefix,
    change_prefix as sys_change_prefix,
    update_google_reactions_wrapper,
)
from resources.core.configure_roles import add_admin_role, remove_admin_role
from resources.core.configure_permissions import ban, unban, global_ban, global_unban
from resources.core.commands.info import info as info_command
from resources.core.evironment import get_version_name
from resources.core.commands.admin_commands import show_guilds as show_guilds_command
from discord import Embed, Role, Member, Emoji, User

from resources.core.permissions import has_admin_permissions
from . import client, get_prefix


@client.command()
async def deny(ctx, member: Member):
    await ban(ctx.message, member)


@client.command()
async def allow(ctx, member: Member):
    await unban(ctx.message, member)


@client.command()
async def global_deny(ctx, user: User):
    await global_ban(ctx.message, user)


@client.command()
async def global_allow(ctx, user: User):
    await global_unban(ctx.message, user)


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
async def info(ctx):
    await info_command(ctx)


@client.command()
async def show_guilds(ctx):
    await show_guilds_command(ctx)


@client.command()
async def help(ctx):
    embed = Embed()

    embed.set_author(
        name="AdriBloober#9372 & TNT2k#7587",
        icon_url="https://pbs.twimg.com/profile_images/843734935022256129/-2pD4h7u_400x400.jpg",
    )
    embed.set_footer(text=f"DiscordSearchBot {get_version_name(get_config())}")

    commands = [
        {
            "name": f"{await get_prefix(None, ctx.message)}help",
            "value": "Hilfe anzeigen",
        },
        {
            "name": f"{await get_prefix(None, ctx.message)}prefix",
            "value": "Prefix anzeigen",
        },
    ]
    admin_commands = [
        {
            "name": f"{await get_prefix(None, ctx.message)}deny @User",
            "value": "Nutzer für Google Anfragen sperren",
        },
        {
            "name": f"{await get_prefix(None, ctx.message)}allow @User",
            "value": "Nutzer für Google Anfragen entsperren",
        },
        {
            "name": f"{await get_prefix(None, ctx.message)}add_role @Role",
            "value": "Eine Admin Rolle hinzufügen",
        },
        {
            "name": f"{await get_prefix(None, ctx.message)}remove_role @Role",
            "value": "Eine Admin Rolle entfernen",
        },
        {
            "name": f"{await get_prefix(None, ctx.message)}change_google_reaction :emoji:",
            "value": "Das Google Reaction Emoji ändern",
        },
        {
            "name": f"{await get_prefix(None, ctx.message)}change_prefix PREFIX",
            "value": "Prefix ändern",
        },
    ]

    for command in commands:
        embed.add_field(name=command["name"], value=command["value"], inline=False)
    if await has_admin_permissions(ctx.guild, ctx.message.author):
        for command in admin_commands:
            embed.add_field(name=command["name"], value=command["value"], inline=False)

    embed.add_field(name="CX Types", value="Mit diesen Commands kannst du googlen: ")

    for cx_type in get_config().ctx_types:
        embed.add_field(
            name=f"{await get_prefix(None, ctx.message)}{cx_type} <search_query>",
            value=f"Auf {cx_type} suchen",
            inline=False,
        )

    await ctx.send(embed=embed)
