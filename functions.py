import re

def getcoords(piece):
    """ Return the correct formatted position from the style str """

    return [int(x) for x in re.findall(r'\d+', piece.get_attribute("style"))]

def tochess(l, color, d):
    """ Converts coord pair to chess notation """

    if color == "black":
        return "hgfedcba"[int(l[0] / d)] + str(1 + int(l[1] / d))
    else:
        return "abcdefgh"[int(l[0] / d)] + str(8 - int(l[1] / d))

def tocoord(s, color, d):
    """ Converts chess notation to coord pair """

    if color == "black":
        return (7 - "abcdefgh".index(s[0])) * d, (int(s[1]) - 1) * d  
    else:
        return "abcdefgh".index(s[0]) * d, (8 - int(s[1])) * d

def validpos(s):
    """ Check if the input is a valid (simplified) chess notation string """
    # disambiguating move
    if len(s) == 5 and s[0] in "nbrkq" and s[1] in "abcdefgh" and s[2] in "12345678" and s[3] in "abcdefgh" and s[4] in "12345678":
        return True
    # pawn disambiguation
    elif len(s) == 4 and s[0] in "abcdefgh" and s[1] in "12345678" and s[2] in "abcdefgh" and s[3] in "12345678":
        return True
    # pawn
    elif len(s) == 2 and s[0] in "abcdefgh" and s[1] in "12345678":
        return True
    # other pieces
    elif len(s) == 3 and s[0] in "nbrkq" and s[1] in "abcdefgh" and s[2] in "12345678":
        return True
    return False
