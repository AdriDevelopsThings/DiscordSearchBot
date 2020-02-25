from ressources.database.server import ServerNotFound


async def parse_error(error, channel):
    if error.__class__ == ServerNotFound:
        await channel.send(f"Der Fehler {error.__class__} ist aufgetreten. Bitte führe @Bot init aus, um den Fehler zu beheben!")
    else:
        await channel.send(
            f"Der Fehler {error.__class__} ist aufgetreten. Bitte informiere die Projektleitung vom DiscordSearchBot!")