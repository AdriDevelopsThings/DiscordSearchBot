from discord.ext.commands import MissingRequiredArgument, BadArgument


async def parse_error(error, channel):
    print(error.__class__)
    if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument):
        await channel.send(
            "Die Argumente wurden falsch gesetzt. Bitte überprüfe diese nochmal und sende den Command erneut!"
        )
        return False
    await channel.send(
        f"Der Fehler {error.__class__} ist aufgetreten. Bitte informiere die Projektleitung vom DiscordSearchBot!"
    )
    return True
