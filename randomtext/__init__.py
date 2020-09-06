import logging
import os
from .model import RandomText
import traceback
import json

log = logging.getLogger("schoolbot.randomtext")

Directory = os.path.dirname(os.path.realpath(__file__))

Texts = {}


def load():
    Failed = []

    for Extension in [File for File in os.listdir(Directory) if File.endswith(".json")]:
        try:
            with open(os.path.join(Directory, "./" + Extension), encoding="UTF8") as fp:
                Texts[os.path.splitext(Extension)[0]] = json.load(fp)
        except:
            log.error(f"while loading randomtext {Extension}, an error occured.")
            traceback.print_exc()
            Failed.append(Extension)

    global Text
    Text = RandomText(Texts)

    return Failed
