import copy

from resources.database.server import get_server


class LanguageDoesNotExists(BaseException):
    pass


def get_available_languages():
    return ["de", "en"]


def get_language_by_guild(guild, s=None):
    return Language(get_server(guild, s).language)


class LanguageReplacement:
    pass


class LanguageElement:
    def __init__(self, value, **replacements):
        self.value = value
        self.replacements = replacements

    def get(self, **replacements) -> str:
        out = copy.deepcopy(self.value)
        for k, v in replacements.items():
            if k in self.replacements:
                out.replace("${" + k + "}", v)
        return out


class LanguageCategory:
    def __init__(self, **elements):
        self.elements = elements


class Language:
    def __init__(self, language_name: str, **categories):
        self.language_name = language_name
        self.categories = categories
        if language_name not in get_available_languages():
            raise LanguageDoesNotExists()


languages = {
    "de": Language(
        "de",
        help=LanguageCategory(
            help_command=LanguageElement("Hilfe anzeigen"),
            prefix_command=LanguageElement("Prefix anzeigen"),
        )
    )
}
