from discord import Emoji

from resources.core.permissions import has_admin_permissions
from resources import client, get_prefix
from resources.database.server import get_server, update_prefix, update_google_reaction


async def msg_prefix(message):
    await message.channel.send(f"Prefix: {await get_prefix(None, message.guild)}")


async def change_prefix(message, new_prefix: str):
    if await has_admin_permissions(message.guild, message.author):
        server = get_server(message.guild)
        if len(new_prefix) == 0 or len(new_prefix) > 10 or new_prefix[0] == "":
            await message.channel.send("Du muss ein neues Präfix angeben!")
            return
        update_prefix(message.guild, new_prefix)
        await message.channel.send(f"Neuer prefix: {new_prefix}")
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")


async def update_google_reactions_wrapper(message, emoji: Emoji):
    if await has_admin_permissions(message.guild, message.author):
        update_google_reaction(message.guild, emoji)
        await message.channel.send(f"Neue Reaction: {emoji}")
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")