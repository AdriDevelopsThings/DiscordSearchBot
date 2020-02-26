from discord import Member

from ressources.core.permissions import has_admin_permissions
from ressources.database.user import add_user, remove_user


async def ban(message, member: Member):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    add_user(member, message.guild)
    await message.channel.send(f"Der Nutzer {member.mention} wurde erfolgreich gebannt!")


async def unban(message, member: Member):
    if not await has_admin_permissions(message.guild, message.author):
        await message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return

    if remove_user(member, message.guild):
        await message.channel.send(f"Der Nutzer {member.mention} wurde entbannt!")
    else:
        await message.channel.send("Der Nutzer ist nicht gebannt!")