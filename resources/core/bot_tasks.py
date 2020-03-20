import discord
import asyncio

from resources import client


async def server_status_update_task():
    while True:
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=f"Active on {str(len(client.guilds))} servers"),
        )
        await asyncio.sleep(60 * 5) # wait 5 Minutes


@client.event
async def on_ready():
    client.loop.create_task(server_status_update_task())
