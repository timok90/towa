import re


class doubleBrackets(object):
    def __init__(self, stringBetween, startindex, endindex):
        self.stringBetween = stringBetween
        self.startindex = startindex
        self.endindex = endindex
        self.vartype = "value"
        self._checkfordot(self.stringBetween)

    def _checkfordot(self, string):
        if string.find(".") > 0:
            self.vartype = "object"
            self.objname = string.split(".")[0]
            self.attrname = string.split(".")[1]
        else:
            self.vartype = "var"


def find_doublebrackets(string):
    p = re.compile("({{).*?(}})")

    brackets = []
    index = 0
    for match in p.finditer(string):

        print(match)

        # get index where the inner string starts and ends
        start = match.regs[1][1]
        end = match.regs[2][0]
        stringbetween = string[start:end]
        stringbetween = stringbetween.strip()
        brackets.append(doubleBrackets(stringbetween, start, end))
        index += 1
    return brackets


def readtext(filepath):

    with open(filepath, "r") as file:
        filetext = file.read()
        brackets = find_doublebrackets(filetext)


if __name__ == "__main__":
    filepath = "C:\\Users\\timok\\Desktop\\TOWA\\Python\\towa\\test_for_template.html"
    readtext(filepath)
