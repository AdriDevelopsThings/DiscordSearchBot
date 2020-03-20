from discord import Guild, TextChannel

from resources.config import get_config
from resources import client


class Logger:
    def __init__(self, guild: Guild, channel: TextChannel):
        self.guild = guild
        self.channel = channel

    async def log(self, message):
        if self.guild is not None:
            await self.channel.send(message)


def get_logger() -> Logger:
    if get_config().LOG_GUILD == None:
        print("Logger does not exists")
        return Logger(None, None)
    guild: Guild = client.get_guild(int(get_config().LOG_GUILD))
    channel: TextChannel = guild.get_channel(int(get_config().LOG_CHANNEL))
    return Logger(guild, channel)
