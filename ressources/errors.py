async def parse_error(error, channel):
    await channel.send(
        f"Der Fehler {error.__class__} ist aufgetreten. Bitte informiere die Projektleitung vom DiscordSearchBot!")
    return True
