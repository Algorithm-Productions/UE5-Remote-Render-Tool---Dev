import eel

eel.init("frontend")


@eel.expose
def connectToServer():
    return False


eel.start("templates/landing.html")
