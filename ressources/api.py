from googleapiclient.discovery import build
from discord import Embed
from .config import get_config


class Api:
    def __init__(self):
        self.service = build("customsearch", "v1", developerKey=get_config().GOOGLE_API_TOKEN)

    def search(self, message):
        search_string = message.content.lstrip("google: ")
        try:
            res = self.service.cse().list(
                q=search_string,
                cx='009036592350705430035:6ldu8w4sb8x'
            ).execute()["items"][:4]
            embed = Embed(title="Google's Ergebnisse für:", description=search_string)
            for i in res:
                embed.add_field(name=i["htmlTitle"].replace("</b>", "").replace("<b>", ""),
                                value=i["formattedUrl"], inline=False)
            embed.set_footer(text=f"Angefragt von {str(message.author)}")
            return embed
        except KeyError:
            return None
