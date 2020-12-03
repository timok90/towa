import re


def find_doublebrackets(string):
    p = re.compile("({{).*?(}})")
    for match in p.finditer(string):
        print(match)


def readtext(filename):

    with open(filepath, "r") as file:
        filetext = file.read()
        find_doublebrackets(filetext)
