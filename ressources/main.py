from discord import Activity, Status
from . import client


@client.event
async def on_ready():
    print("Ready")
    activity = Activity(name="Geil")
    await client.change_presence(activity=activity, status=Status.idle)
