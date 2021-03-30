class style:
    """ Explanation:
    How to use style? Use f-string like this:
    f"Here is normal text {style.tRED} and here is colorful text {style.RESET}. Here is normal again."

    Key to the names:
    t... is the color of the text; example: tRED == text is RED)
    b... is the color of the background; example: bYELLOW == background is YELLOW
    f... is the type of font; example: fBOLD == font is BOLD
    t...b... is the hybrid; example: tREDbYELLOW == text is RED and background is YELLOW
    """
    RESET = '\033[0m'

    tRED = '\033[91m'
    tGREEN = '\033[92m'
    tYELLOW = '\033[93m'
    tBLUE = '\033[94m'


    bBLACK = '\033[40m'
    bGREY = '\033[100m'

    fBOLD = '\033[1m'
    fUNDERLINE = '\033[4m'