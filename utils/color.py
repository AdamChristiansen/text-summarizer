"""
This module provide a set of functions for printing in color using ANSII
escape sequences.
"""

NRM = "\033[0m"  # Normal
BLK = "\033[30m" # Black
RED = "\033[31m" # Red
GRN = "\033[32m" # Green
YEL = "\033[33m" # Yellow
BLU = "\033[34m" # Blue
MAG = "\033[35m" # Magenta
CYN = "\033[36m" # Cyan
WHT = "\033[37m" # White

nrm = lambda s: "{}{}{}".format(NRM, s, NRM)
blk = lambda s: "{}{}{}".format(BLK, s, NRM)
red = lambda s: "{}{}{}".format(RED, s, NRM)
grn = lambda s: "{}{}{}".format(GRN, s, NRM)
yel = lambda s: "{}{}{}".format(YEL, s, NRM)
blu = lambda s: "{}{}{}".format(BLU, s, NRM)
mag = lambda s: "{}{}{}".format(MAG, s, NRM)
cyn = lambda s: "{}{}{}".format(CYN, s, NRM)
wht = lambda s: "{}{}{}".format(WHT, s, NRM)
