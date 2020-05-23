from typing import List
from urllib.parse import quote

from discord.ext.commands import MissingRequiredArgument


async def lmgtfy_api(ctx, *questions_raw):
    questions: List[str] = []
    for question_raw in questions_raw:
        if type(question_raw) == tuple:
            for question_raw_tuple in question_raw:
                questions.append(question_raw_tuple)
        else:
            questions.append(question_raw)
    if len(questions) == 0:
        raise MissingRequiredArgument("search_query")
    link = "https://lmgtfy.com/?q="
    for question in questions:
        link += quote(question) + "+"
    await ctx.send(link[:len(link) - 1])
