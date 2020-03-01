from resources import get_config, get_prefix
from resources.core.evironment import get_version_name
from discord import Embed


async def info(ctx):
    embed = Embed(title="DiscordSearchBot Info")
    embed.set_author(name="AdriBloober#9372 & TNT2k#7587")
    embed.set_footer(text=f"Apache License 2020")

    explanation_fields = [
        {"name": "Beschreibung",
         "value": "Der SearchBot ist ein Bot, mit dem man nach verschiedenene Dingen suchen kann."},
        {"name": "Prefix", "value": await get_prefix(None, ctx.message)},
        {"name": "Version", "value": get_version_name(get_config())},
        {"name": "GitHub", "value": get_config().github_link},
        {"name": "Authors", "value": "OpenSource Projekt von AdriBloober#9372 und TNT2k7587"}
    ]

    for field in explanation_fields:
        embed.add_field(name=field["name"], value=field["value"], inline=False)

    await ctx.send(embed=embed)
