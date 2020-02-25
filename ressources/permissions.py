from ressources.database.role import get_roles
from ressources.database.server import get_server, update_server
from ressources.database.server import join_server as create_server
from . import get_config, client
from .database.user import get_user, add_user, remove_user


async def get_prefix(guild):
    return get_server(guild.id)


async def has_admin_permissions(guild, member):
    roles = get_roles(guild.id)
    if roles:
        for role in roles:
            for member_role in member.roles:
                if member_role.id == role.admin_role_id:
                    return True
    return False


async def is_allowed_to_use(message):
    if len(get_user(message.author.id, message.guild.id)) > 0:
        return False
    return True


async def join_server(guild, message=None):
    if not message is None and not await has_admin_permissions(
        message.guild, message.author
    ):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    server = create_server(guild.id)
    if not message is None:
        await message.channel.send(
            f"Der Server wurde erfolgreich initalisiert. Der Prefix ist {server.prefix}"
        )


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
    add_user(user, message.guild.id)
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
    if remove_user(user, message.guild.id):
        await message.channel.send(f"Der Nutzer <@!{user}> wurde entbannt!")
    else:
        await message.channel.send("Der Nutzer ist nicht gebannt!")


async def prefix(message):
    if await has_admin_permissions(message.guild, message.author):
        await message.channel.send(f"Prefix: {get_prefix(message.guild)}")


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
        update_server(message.id, {"prefix": new_prefix})
        await message.channel.send(f"Neuer prefix: {new_prefix}")
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
