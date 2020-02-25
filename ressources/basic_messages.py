from urllib.parse import quote

from discord import Embed

from . import client, api, get_config
from .permissions import is_allowed_to_use, prefix, change_prefix, ban, unban

already_processed_requests = []

async def google_message(message, name):
    if not await is_allowed_to_use(message):
        await message.add_reaction("❌")
        return
    response = api.search(message, name)
    await message.channel.send(embed=response)


async def get_google_command(message):
    for type in get_config().ctx_types:
        if message.content.startswith(f"{type}: "):
            await google_message(message, type)


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    await get_google_command(message)

    if message.content.startswith("lmgtfy: "):
        if not await is_allowed_to_use(message):
            await message.add_reaction("❌")
            return

        await message.channel.send(
            "https://lmgtfy.com/?q="
            + quote(message.content.lstrip("lmgtfy: ")).replace("%20", "+")
        )

    elif message.content.startswith(f"<@!{client.user.id}> changeprefix"):
        await change_prefix(message)

    elif message.content.startswith(f"<@!{client.user.id}> prefix"):
        await prefix(message)

    elif message.content.startswith(f"<@!{client.user.id}> deny"):
        await ban(message)

    elif message.content.startswith(f"<@!{client.user.id}> allow"):
        await unban(message)

    elif message.content == f"<@!{client.user.id}> reload":
        if (
            message.author.id == 330148908531580928
            or message.author.id == 212866839083089921
        ):
            get_config().load_config_from_file()
            await message.channel.send(
                f"{message.author.mention} Reload abgeschlossen."
            )

    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user):
    if user.id == client.user.id:
        return
    if not await is_allowed_to_use(reaction.message):
        await reaction.message.add_reaction("❌")
        return

    if reaction.count != 1 or reaction.message.id in already_processed_requests:
        return

    if str(reaction) in [
        "<:google:331075369501196290>",
        "<:google:677939519160451093>",
    ]:
        response = api.search(reaction.message)
        already_processed_requests.append(reaction.message.id)
        await reaction.message.channel.send(embed=response)
