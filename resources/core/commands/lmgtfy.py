from urllib.parse import quote


def lmgtfy_api(ctx, q):
    ctx.send("https://lmgtfy.com/?q=" + quote(q).replace("%20", "+"))
