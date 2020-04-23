from typing import List

from discord import TextChannel, Message

from resources.core.configure_permissions import ban
from resources import client


class BanMessageTemplate:
    def __init__(self, author, guild, channel: TextChannel):
        self.author = author
        self.guild = guild
        self.channel = channel


class SubmitedTask:
    def __init__(self, message: Message, author, type, orginal_message=None):
        self.message = message
        self.author_id = author.id
        self.type = type
        self.orginal_message = orginal_message

    async def kill(self, ban_msg_template: BanMessageTemplate):
        await ban(ban_msg_template, client.get_user(self.author_id))
        await self.message.edit(
            content=":x: Dieser Inhalt wurde entfernt :x:", embed=None
        )


tasks: List[SubmitedTask] = []


def add_task(task: SubmitedTask):
    tasks.append(task)


def remove_task(task: SubmitedTask):
    tasks.remove(task)


def get_task_by_message(message):
    for task in tasks:
        if task.message.id == message.id:
            return task

def get_task_by_orginal_message(message):
    for task in tasks:
        if task.orginal_message.id == message.id:
            return task