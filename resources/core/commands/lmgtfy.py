from urllib.parse import quote


async def lmgtfy_api(ctx, q):
    await ctx.send("https://lmgtfy.com/?q=" + quote(q).replace("%20", "+"))
