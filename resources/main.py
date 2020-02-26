from discord import Activity, Status
from . import client


@client.event
async def on_ready():
    print("Ready")
    activity = Activity(name="Crawling gooooogle...")
    await client.change_presence(activity=activity, status=Status.online)
