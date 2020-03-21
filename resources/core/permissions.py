from resources.database.role import get_roles
from resources.database.user import get_user, add_user, remove_user


async def has_admin_permissions(guild, member):
    roles = get_roles(guild)
    if is_gloabl_admin(member):
        return True
    if any(map(lambda permission: permission == ("administrator", True), member.guild_permissions)):
        return True
    if roles:
        return any(
            [any(map(lambda member_role: str(role.admin_role_id) == str(member_role.id), member.roles)) for role in roles])
    return False


async def is_allowed_to_use(user, guild):
    if len(get_user(user, guild)) > 0:
        return False
    return True


def is_gloabl_admin(user):
    admins = [
        330148908531580928,  # AdriBloober
        212866839083089921  # TNT2k
    ]
    return user.id in admins
