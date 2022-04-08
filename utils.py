from colored import stylize
from datetime import datetime
import colored
import json


class Logger:
    def __init__(self, title, id_num=None):
        if id_num is None:
            self.identifier = "[{}]".format(title)
        else:
            self.identifier = "[{} {}]".format(title, id_num)

    def generate_text(self, identifier, tag, msg):
        timestamp_now = datetime.now()
        timestamp_string = f"{timestamp_now:%I:%M:%S.%f %p}"
        return f"[{timestamp_string}] {identifier} [{tag}] -> {msg}"

    def alert(self, msg, tag="ALERT"):
        text = self.generate_text(self.identifier, tag, msg)
        print(stylize(text, colored.fg("magenta")), flush=True)

    def info(self, msg, tag="INFO"):
        text = self.generate_text(self.identifier, tag, msg)
        print(stylize(text, colored.fg("cyan")), flush=True)

    def error(self, msg, tag="ERROR"):
        text = self.generate_text(self.identifier, tag, msg)
        print(stylize(text, colored.fg("red")), flush=True)

    def success(self, msg, tag="SUCCESS"):
        text = self.generate_text(self.identifier, tag, msg)
        print(stylize(text, colored.fg("green")), flush=True)


def read_config(filename):
    with open(filename, "r") as config:
        return json.load(config)
