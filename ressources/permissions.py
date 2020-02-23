from . import get_config, get_prefix, client
from .database.user import get_user, add_user, remove_user


async def has_admin_permissions(guild, member):
    roles: list = get_config().role_settings.get(str(guild.id))
    if roles:
        return any(guild.get_role(int(f)) in member.roles for f in roles) or str(member.id) in roles
    return False


async def is_allowed_to_use(message):
    if len(get_user(message.author.id, message.guild.id)) > 0:
        return False
    return True


async def ban(message):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    if len(message.mentions) != 1:
        await message.channel.send("Kein User angegeben oder das Kommando ist falsch aufgebaut!")
        return
    user = message.mentions[0].id
    add_user(user, message.guild.id)
    await message.channel.send(f"Der Nutzer <@!{user}> wurde erfolgreich gebannt!")


async def unban(message):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    if len(message.mentions) != 1:
        await message.channel.send("Kein User angegeben oder das Kommando ist falsch aufgebaut!")
        return

    user = message.mentions[0].id
    if remove_user(user, message.guild.id):
        await message.channel.send(f"Der Nutzer <@!{user}> wurde entbannt!")
    else:
        await message.channel.send("Der Nutzer ist nicht gebannt!")


async def prefix(message):
    if await has_admin_permissions(message.guild, message.author):
        await message.channel.send(f"Prefix: {get_prefix(None, message)}")


async def change_prefix(message):
    if await has_admin_permissions(message.guild, message.author):
        new_prefix = message.content.replace(f"<@!{client.user.id}> changeprefix", "") \
            .replace("\n", "").replace("\t", "").lstrip(" ").split(" ")
        if len(new_prefix) == 0 or new_prefix[0] == "":
            await message.channel.send("Du muss ein neues Präfix angeben!")
            return
        new_prefix = new_prefix[0]
        get_config().prefixes.update({message.guild.id: new_prefix})
        get_config().save_to_json()
        await message.channel.send(f"New prefix: {new_prefix}")
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
