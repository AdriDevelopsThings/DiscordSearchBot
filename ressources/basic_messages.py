from urllib.parse import quote
from .database.server import get_server

from . import client, api, get_config
import traceback
from ressources.errors import parse_error
from .permissions import is_allowed_to_use, prefix, change_prefix, ban, unban

already_processed_request_id = []


async def google_message(message, name):
    already_processed_request_id.append(message.id)
    if not await is_allowed_to_use(message):
        await message.add_reaction("❌")
        return
    response = api.search(message, name)
    await message.channel.send(embed=response)


async def get_google_command(message):
    for type in get_config().ctx_types:
        if message.content.startswith(f"{type}: "):
            await google_message(message, type)


def get_mention():
    return f"<@!{client.user.id}>"


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    try:
        await get_google_command(message)
        if message.content.startswith("lmgtfy: "):
            if not await is_allowed_to_use(message):
                await message.add_reaction("❌")
                return

            await message.channel.send(
                "https://lmgtfy.com/?q="
                + quote(message.content.lstrip("lmgtfy: ")).replace("%20", "+")
            )

        elif message.content.startswith(f"{get_mention()} changeprefix"):
            await change_prefix(message)

        elif message.content.startswith(f"{get_mention()} prefix"):
            await prefix(message)

        elif message.content.startswith(f"{get_mention()} deny"):
            await ban(message)

        elif message.content.startswith(f"{get_mention()} allow"):
            await unban(message)

    except Exception as e:
        await parse_error(e, message.channel)
        traceback.print_exc()

    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user):
    if user.id == client.user.id:
        return
    if not await is_allowed_to_use(reaction.message):
        await reaction.message.add_reaction("❌")
        return

    if reaction.count != 1 or reaction.message.id in already_processed_request_id:
        return

    google_reaction = get_server(reaction.message.guild).google_reaction
    if str(reaction) == google_reaction:
        response = api.search(reaction.message)
        already_processed_request_id.append(reaction.message.id)
        await reaction.message.channel.send(embed=response)
