import os


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")
