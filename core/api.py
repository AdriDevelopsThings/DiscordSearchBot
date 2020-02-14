import pprint

from googleapiclient.discovery import build
import settings
class Api:
    def __init__(self):
        pass
    def ini(self):
        self.service = build("customsearch", "v1", developerKey=settings.GOOGLE_API_TOKEN.get_string())
    def search(self, q):
        try:
            res = self.service.cse().list(
                q=q,
                cx='009036592350705430035:6ldu8w4sb8x'
            ).execute()["items"][:4]
            out = []
            for i in res:
                out.append({"title": i["htmlTitle"].replace("</b>", "").replace("<b>", ""), "link": i["formattedUrl"]})
            return out
        except KeyError:
            return None
