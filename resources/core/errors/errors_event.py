from resources import client
from .errors import parse_error
import traceback


@client.event
async def on_command_error(ctx, exception):
    if await parse_error(exception, ctx.channel):
        traceback.print_exc()
