from json import load, dumps


def read(filename="banlist.json"):
    j = {}
    with open(filename, "r") as file:
        j = load(file)
    return j


def write(j, filename="banlist.json"):
    j = dumps(j)
    with open(filename, "w") as file:
        file.write(j)
