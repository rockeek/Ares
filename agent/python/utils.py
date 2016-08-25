import requests
import re

import settings


def send_output(output):
    requests.post(settings.SERVER_URL + "/api/report", {'botid': settings.BOT_ID, 'output': output})
    if settings.DEBUG:
        print output


def validate_botid(candidate):
    return re.match('^[a-zA-Z0-9\s\-_]+$', candidate) is not None
    
