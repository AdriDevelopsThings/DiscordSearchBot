from resources.database.role import get_roles
from resources.database.user import get_user, add_user, remove_user


async def has_admin_permissions(guild, member):
    roles = get_roles(guild)
    if any(map(lambda permission: permission == ("administrator", True), member.guild_permissions)):
        return True
    if roles:
        return any([any(map(lambda member_role: str(role.admin_role_id) == str(member_role.id), member.roles)) for role in roles])
    return False


async def is_allowed_to_use(message):
    if len(get_user(message.author, message.guild)) > 0:
        return False
    return True


