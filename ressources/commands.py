from .permissions import has_admin_permissions, ban, unban
from . import client


@client.command()
async def deny(ctx):
    if not await has_admin_permissions(ctx.message.guild, ctx.message.author):
        await ctx.message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    if len(ctx.message.mentions) != 1:
        await ctx.message.channel.send(
            "Kein User angegeben oder das Kommando ist falsch aufgebaut!"
        )
        return
    user = ctx.message.mentions[0].id
    await ban(user, ctx.message.guild)
    await ctx.message.channel.send(f"Der Nutzer <@!{user}> wurde erfolgreich gebannt!")


@client.command()
async def allow(ctx):
    if not await has_admin_permissions(ctx.message.guild, ctx.message.author):
        await ctx.message.channel.send("Du hast keine Erlaubnis, das auszuführen!")
        return
    if len(ctx.message.mentions) != 1:
        await ctx.message.channel.send(
            "Kein User angegeben oder das Kommando ist falsch aufgebaut!"
        )
        return
    user = ctx.message.mentions[0].id

    allow_success = await unban(user, ctx.message.guild)
    if allow_success:
        await ctx.message.channel.send(f"Der Nutzer <@!{user}> wurde entbannt!")
    else:
        await ctx.message.channel.send("Der Nutzer ist nicht gebannt!")
