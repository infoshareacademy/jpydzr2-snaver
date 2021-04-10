class style:
    """ Explanation how to use styles:
    Use f-string like this:
    f"Here is normal text {style.tRED} and here is colorful text {style.RESET}. Here is normal again."
    Key to the names:
    t... is the color of the text; example: tRED == text is RED)
    b... is the color of the background; example: bYELLOW == background is YELLOW
    t...b... is the hybrid; example: tREDbYELLOW == text is RED and background is YELLOW
    f... is the type of font; example: fBOLD == font is BOLD
    """
    RESET = '\033[0m'

    tBLACK = '\033[30m'
    tRED = '\033[91m'
    tGREEN = '\033[92m'
    tYELLOW = '\033[93m'
    tBLUE = '\033[94m'

    bBLACK = '\033[40m'
    bGREY = '\033[100m'
    bYELLOW = '\033[103m'

    tREDbYELLOW = '\033[91m\033[103m'

    fBOLD = '\033[1m'
    fUNDERLINE = '\033[4m'