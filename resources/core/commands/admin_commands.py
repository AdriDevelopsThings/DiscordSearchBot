from resources import client
from resources.core.permissions import is_gloabl_admin


async def show_guilds(ctx):
    if is_gloabl_admin(ctx.message.author):
        out = ""
        for guild in client.guilds:
            out += f"``{guild.name}`` -> ``{client.get_user(guild.owner_id).name}``\n"
        await ctx.send(out)
    else:
        await ctx.send("Du hast keine Erlaubnis, das auszuführen!")
