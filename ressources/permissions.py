from ressources.database.role import get_roles
from ressources.database.server import update_prefix, update_google_reaction
from .database.user import get_user, add_user, remove_user
from . import client, get_prefix


async def has_admin_permissions(guild, member):
    roles = get_roles(guild)
    if roles:
        [any(map(lambda member_role: str(role.admin_role_id) == str(member_role.id), member.roles)) for role in roles]
    return False


async def is_allowed_to_use(message):
    if len(get_user(message.author.id, message.guild)) > 0:
        return False
    return True


async def ban(message):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    if len(message.mentions) != 1:
        await message.channel.send(
            "Kein User angegeben oder das Kommando ist falsch aufgebaut!"
        )
        return
    user = message.mentions[0].id
    add_user(user, message.guild)
    await message.channel.send(f"Der Nutzer <@!{user}> wurde erfolgreich gebannt!")


async def unban(message):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    if len(message.mentions) != 1:
        await message.channel.send(
            "Kein User angegeben oder das Kommando ist falsch aufgebaut!"
        )
        return

    user = message.mentions[0].id
    if remove_user(user, message.guild):
        await message.channel.send(f"Der Nutzer <@!{user}> wurde entbannt!")
    else:
        await message.channel.send("Der Nutzer ist nicht gebannt!")


async def prefix(message):
    if await has_admin_permissions(message.guild, message.author):
        await message.channel.send(f"Prefix: {get_prefix(None, message.guild)}")


async def change_prefix(message):
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
        update_prefix(message.guild, new_prefix)
        await message.channel.send(f"Neuer prefix: {new_prefix}")
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")


async def update_google_reactions_wrapper(message):
    if await has_admin_permissions(message.guild, message.author):
        new_google_reaction = (
            message.content.replace(f"<@!{client.user.id}> changereaction", "")
            .replace("\n", "")
            .replace("\t", "")
            .lstrip(" ")
            .split(" ")
        )
        if len(new_google_reaction) == 0 or new_google_reaction[0] == "":
            await message.channel.send("Du muss eine neue Reaction angeben!")
            return
        new_google_reaction = new_google_reaction[0]
        update_google_reaction(message.guild, new_google_reaction)
        await message.channel.send(f"Neue reaction: {new_google_reaction}")
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
