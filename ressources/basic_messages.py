from urllib.parse import quote
from . import client, api, get_config, get_prefix
from .permissions import is_allowed_to_use, has_admin_permissions

already_processed_requests = []


async def google_message(message, name):
    if not await is_allowed_to_use(message):
        await message.add_reaction("❌")
        return
    response = api.search(message, name)
    if response is None:
        await message.channel.send("0 Ergebnisse gefunden")
    else:
        await message.channel.send(embed=response)


async def get_google_command(message):
    types = ["google", "stackoverflow"]
    for type in types:
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
        if await has_admin_permissions(message.guild, message.author):
            new_prefix = (
                message.content.replace(f"<@!{client.user.id}> changeprefix", "")
                .replace("\n", "")
                .replace("\t", "")
                .lstrip(" ")
                .split(" ")
            )
            if len(new_prefix) == 0 or new_prefix[0] == "":
                await message.channel.send("Du muss ein neues Präfix angeben!")
                return
            new_prefix = new_prefix[0]
            get_config().prefixes.update({message.guild.id: new_prefix})
            get_config().save_to_json()
            await message.channel.send(f"New prefix: {new_prefix}")
        else:
            await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")

    elif message.content.startswith(f"<@!{client.user.id}> prefix"):
        if await has_admin_permissions(message.guild, message.author):
            await message.channel.send(f"Prefix: {get_prefix(None, message)}")

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
        if response is None:
            await reaction.message.channel.send("0 Ergebnisse gefunden")
        else:
            await reaction.message.channel.send(embed=response)
