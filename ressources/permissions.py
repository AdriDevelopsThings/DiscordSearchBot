from . import get_config
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


async def ban(user_id, guild):
    add_user(user_id, guild.id)


async def unban(user_id, guild):
    return remove_user(user_id, guild.id)
