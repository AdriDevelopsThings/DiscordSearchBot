from time import sleep

from discord import Forbidden, User, NotFound

from .database.server import get_server
from resources.core.logger import get_logger

from . import client, api, get_config
import traceback
from resources.core.errors.errors import parse_error
from resources.core.permissions import is_allowed_to_use, has_admin_permissions
from resources.core.configure import msg_prefix, change_prefix
from resources import get_prefix
from datetime import datetime
from resources.core.submited_tasks import SubmitedTask, BanMessageTemplate, add_task, get_task_by_message, remove_task, \
    get_task_by_orginal_message

already_processed_request_id = []


async def google_message(message, name):
    already_processed_request_id.append(message.id)
    if not await is_allowed_to_use(message.author, message.guild):
        await message.add_reaction("❌")
        return
    msg = await api.search(message, message.channel, search_type="command", cx_type=name, prefix=await get_prefix(None, message))
    await msg.add_reaction(b'\xf0\x9f\x97\x91\xef\xb8\x8f'.decode())
    add_task(SubmitedTask(msg, message.author, "command", orginal_message=message))


async def get_google_command(message):
    for type in get_config().ctx_types:
        if message.content.startswith(f"{await get_prefix(None, message)}{type} "):
            await google_message(message, type)


def check_message_validity(message) -> bool:
    created_at = message.created_at
    now = datetime.now()
    days = (now - created_at).days
    return days < get_config().message_reacting_expire


def get_mention():
    return f"<@!{client.user.id}>"


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    try:
        await get_google_command(message)
        if message.content.startswith(f"{get_mention()} prefix"):
            await msg_prefix(message)

    except Exception as e:
        if await parse_error(e, message.channel):
            traceback.print_exc()
    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user: User):
    if user.id == client.user.id:
        return
    if str(reaction) == "❌" and await has_admin_permissions(reaction.message.guild, user):
        task = get_task_by_message(reaction.message)
        if not task is None:
            await reaction.remove(user)
            await task.kill(BanMessageTemplate(user, reaction.message.guild, reaction.message.channel))
    if not user.bot and reaction.emoji.encode() == b'\xf0\x9f\x97\x91\xef\xb8\x8f' and reaction.count > 1:
        task = get_task_by_message(reaction.message)
        if task is not None:
            if task.author_id == user.id:
                if task.orginal_message is not None:
                    try:
                        await task.orginal_message.delete()
                    except Forbidden:
                        await reaction.message.channel.send("Liebe Admins, ich habe ja schon wenig Rechte, nur bitte "
                                                            "bitte bitte gebt mir Rechte, um Nachrichten zu löschen. "
                                                            ":cry: Ich wäre euch sehr dankbar!")
                    finally:
                        await reaction.message.delete()
                        remove_task(task)
            else:
                await reaction.remove(user)

    if not await is_allowed_to_use(user, reaction.message.guild):
        await reaction.message.add_reaction("❌")
        return

    if (
            reaction.count > 3
            or reaction.message.id in already_processed_request_id
            or not check_message_validity(reaction.message)
    ):
        return

    google_reaction = get_server(reaction.message.guild).google_reaction
    if google_reaction is None or google_reaction == "":
        emoji = None
    else:
        emoji = client.get_emoji(int(google_reaction))
    if type(reaction.emoji) == str:
        return
    if emoji and reaction.emoji.id == emoji.id:
        message = await api.search(reaction.message, reaction.message.channel,  search_type="reaction", reaction_user=user)
        already_processed_request_id.append(reaction.message.id)
        await message.add_reaction(b'\xf0\x9f\x97\x91\xef\xb8\x8f'.decode())
        add_task(SubmitedTask(message, user, "reaction"))


@client.event
async def on_guild_join(guild):
    logger = get_logger()
    await logger.log(f"Juhu! Der Server '{guild.name}' nutzt nun den DiscordSearchBot!")

@client.event
async def on_message_delete(message):
    task = get_task_by_orginal_message(message)
    if task is not None:
        try:
            await task.message.delete()
        except NotFound:
            pass
        finally:
            remove_task(task)