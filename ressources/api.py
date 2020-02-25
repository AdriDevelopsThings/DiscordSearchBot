from googleapiclient.discovery import build
from discord import Embed
from .config import get_config


class GoogleCxNotFound(BaseException):
    pass


def strip_search_query(message_content, cx_type):
    search_query = message_content.lstrip(f"{cx_type}:")
    if search_query[0] == " ":
        search_query = search_query[1:]
    return search_query


class Api:
    def __init__(self):
        self.service = build(
            "customsearch", "v1", developerKey=get_config().GOOGLE_API_TOKEN
        )

    def get_cx_by_name(self, name):
        if name == "google":
            return get_config().GOOGLE_CX_ALL
        elif name == "stackoverflow":
            return get_config().GOOGLE_CX_STACKOVERFLOW
        else:
            raise GoogleCxNotFound()

    def parse_search_to_embed(self, resource, message, search_string):
        embed = Embed(title="Google's Ergebnisse für:", description=search_string)
        for i in resource:
            embed.add_field(
                name=i["htmlTitle"].replace("</b>", "").replace("<b>", ""),
                value=i["link"],
                inline=False,
            )
        embed.set_footer(text=f"Angefragt von {str(message.author)}")
        return embed

    def search(self, message, cx_type="google"):
        search_string = strip_search_query(message.content, cx_type)
        try:
            res = (
                self.service.cse()
                .list(q=search_string, cx=self.get_cx_by_name(cx_type))
                .execute()["items"][:4]
            )
            return self.parse_search_to_embed(res, message, search_string)
        except KeyError:
            return None
