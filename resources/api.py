import requests
from discord.ext.commands import MissingRequiredArgument
from googleapiclient.discovery import build
from urllib.parse import quote
from discord import Embed
from .config import get_config


class GoogleCxNotFound(BaseException):
    pass


def strip_search_query(message_content, cx_type, prefix):
    search_query = message_content.lstrip(f"{prefix}{cx_type}")
    if search_query[0] == " ":
        search_query = search_query[1:]
    return search_query


class Api:
    def __init__(self):
        self.service = build(
            "customsearch", "v1", developerKey=get_config().GOOGLE_API_TOKEN
        )

    def duckduckgo_search(self, q):
        response = requests.get(
            f"https://api.duckduckgo.com/?q={quote(q)}&format=json&pretty=1"
        ).json()

    def lmgtfy_search(self, q):
        if len(q) == 0:
            raise MissingRequiredArgument("search_query")
        link = "https://lmgtfy.com/?q="
        for question in q.split():
            link += quote(question) + "+"
        return link[:len(link) - 1]

    def get_not_found_message(self, user, search_string, search_type):
        embed = Embed(
            title="Google's Ergebnisse für:", description=search_string, color=0xFF0000
        )
        embed.add_field(name="Fehler", value="Es wurde kein Ergebniss gefunden.")
        embed.set_footer(text=f"Angefragt von {str(user)} via {search_type}")
        return embed

    def get_cx_by_name(self, name):
        if name == "google":
            return get_config().GOOGLE_CX_ALL
        elif name == "stackoverflow":
            return get_config().GOOGLE_CX_STACKOVERFLOW
        elif name == "wikipedia":
            return get_config().GOOGLE_CX_WIKIPEDIA
        elif name == "youtube":
            return get_config().GOOGLE_CX_YOUTUBE
        else:
            raise GoogleCxNotFound()

    def parse_search_to_embed(
        self, resource, message, search_string, search_type=None, reaction_user=None
    ):
        embed = Embed(title="Google's Ergebnisse für:", description=search_string)
        for i in resource:
            embed.add_field(
                name=i["htmlTitle"].replace("</b>", "").replace("<b>", ""),
                value=i["link"],
                inline=False,
            )
        if reaction_user is None:
            embed.set_footer(
                text=f"Angefragt von {str(message.author)} via {search_type}"
            )
        else:
            embed.set_footer(
                text=f"Angefragt von {str(reaction_user)} via {search_type}"
            )
        return embed

    async def search(
        self,
        message,
        channel,
        search_type="command",
        cx_type="google",
        reaction_user=None,
        prefix="§",
    ):
        if search_type == "command":
            search_string = strip_search_query(message.content, cx_type, prefix)
        else:
            search_string = message.content

        if cx_type == "duckduckgo" or cx_type == "ddg":
            self.duckduckgo_search(search_string)
        elif cx_type == "lmgtfy":
            return await channel.send(self.lmgtfy_search(search_string))

        try:
            res = (
                self.service.cse()
                .list(q=search_string, cx=self.get_cx_by_name(cx_type))
                .execute()["items"][:4]
            )
            return await channel.send(embed=self.parse_search_to_embed(
                res,
                message,
                search_string,
                reaction_user=reaction_user,
                search_type=search_type,
            ))
        except KeyError:
            if search_type == "reaction":
                return await channel.send(embed=self.get_not_found_message(
                    reaction_user, search_string, search_type=search_type
                ))
            else:
                return await channel.send(embed=self.get_not_found_message(
                    message.author, search_string, search_type=search_type
                ))
