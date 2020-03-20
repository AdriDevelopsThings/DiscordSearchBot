from discord.ext.commands import MissingRequiredArgument, BadArgument, CommandNotFound, CommandInvokeError

from resources.core.logger import get_logger


async def send_error_to_log(error, guild):
    logger = get_logger()
    await logger.log(f"Auf dem Server {guild.name} ist der Fehler {error.__class__} aufgetreten.")


async def parse_error(error, channel):
    if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument):
        await channel.send(
            "Die Argumente wurden falsch gesetzt. Bitte überprüfe diese nochmal und sende den Command erneut!"
        )
        return False
    elif isinstance(error, CommandNotFound):
        return False
    elif isinstance(error, CommandInvokeError):
        print(error.__cause__)
        await send_error_to_log(error, channel.guild)
        await channel.send(
            f"Der Fehler {error.__cause__} ist aufgetreten. Bitte informiere die Projektleitung vom DiscordSearchBot!"
        )
        return True
    await send_error_to_log(error, channel.guild)
    await channel.send(
        f"Der Fehler {error.__class__} ist aufgetreten. Bitte informiere die Projektleitung vom DiscordSearchBot!"
    )
    return True
