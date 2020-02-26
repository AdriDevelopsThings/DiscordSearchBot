from resources.core.permissions import has_admin_permissions
from resources.database.role import add_role, remove_role, get_roles


def check_if_role_exists(guild, discord_role):
    roles = get_roles(guild)
    return any(map(lambda role: role.admin_role_id == str(discord_role.id), roles))


async def add_admin_role(message, role):
    if await has_admin_permissions(message.guild, message.author):

        if check_if_role_exists(message.guild, role):
            return await message.channel.send(
                f"Die Rolle {role} ist bereits als admin_role markiert!"
            )

        add_role(message.guild, role)
        await message.channel.send(
            f"Die Rolle {role} wurde erfolgreich als admin_role markiert!"
        )
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")


async def remove_admin_role(message, role):
    if await has_admin_permissions(message.guild, message.author):
        if not check_if_role_exists(message.guild, role):
            return await message.channel.send(
                f"Die Rolle {role} ist nicht als admin_role markiert!"
            )
        remove_role(message.guild, role)
        await message.channel.send(f"Die Rolle {role} wurde erfolgreich entfernt.")
    else:
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
