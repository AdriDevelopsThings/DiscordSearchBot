from discord import Member, User

from resources.core.permissions import has_admin_permissions, is_gloabl_admin
from resources.database.user import (
    add_user,
    remove_user,
    add_gloabl_user,
    remove_global_user,
)


async def ban(message, member: Member):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    add_user(member, message.guild)
    await message.channel.send(
        f"Der Nutzer {member.mention} wurde erfolgreich gebannt!"
    )


async def unban(message, member: Member):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return

    if remove_user(member, message.guild):
        await message.channel.send(f"Der Nutzer {member.mention} wurde entbannt!")
    else:
        await message.channel.send("Der Nutzer ist nicht gebannt!")


async def global_ban(message, user: User):
    if not is_gloabl_admin(message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    add_gloabl_user(user)
    await message.channel.send(
        f"Der Nutzer {user.mention} wurde erfolgreich gloabl gebannt!"
    )


async def global_unban(message, user: User):
    if not is_gloabl_admin(message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    if remove_global_user(user):
        await message.channel.send(
            f"Der Nutzer {user.mention} wurde erfolgreich gloabl entbannt!"
        )
    else:
        await message.channel.send("Der Nutzer ist nicht global gebannt!")
