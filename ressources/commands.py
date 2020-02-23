from .permissions import ban, unban, prefix, change_prefix
from . import client


@client.command()
async def deny(ctx):
    await ban(ctx.message)


@client.command()
async def allow(ctx):
    await unban(ctx.message)


@client.command()
async def prefix(ctx):
    await prefix(ctx.message)


@client.command()
async def change_prefix(ctx):
    await change_prefix(ctx.message)
