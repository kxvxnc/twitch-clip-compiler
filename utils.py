from colored import stylize
from datetime import datetime
import colored
import json
import requests

class Logger:
    def __init__(self, title, id_num=None):
        if id_num == None:
            self.identifier = "[{}]".format(title)
        else:
            self.identifier = "[{} {}]".format(title, id_num)

    def alert(self, msg, tag="ALERT"):
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        text = "[{}] {} [{}] -> {}".format(current_time, self.identifier, tag, msg)
        print(stylize(text, colored.fg("magenta")), flush=True)

    def info(self, msg, tag="INFO"):
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        text = "[{}] {} [{}] -> {}".format(current_time, self.identifier, tag, msg)
        print(stylize(text, colored.fg("cyan")), flush=True)

    def error(self, msg, tag="ERROR"):
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        text = "[{}] {} [{}] -> {}".format(current_time, self.identifier, tag, msg)
        print(stylize(text, colored.fg("red")), flush=True)

    def success(self, msg ,tag="SUCCESS"):
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        text = "[{}] {} [{}] -> {}".format(current_time, self.identifier, tag, msg)
        print(stylize(text, colored.fg("green")), flush=True)

logger = Logger("DOWNLOAD")

def read_config(filename):
    with open(filename, "r") as config:
        return json.load(config)

def download_video(url, output_path):
    logger.alert(f"\nDownloading {url} -> {output_path}")
    r = requests.get(url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size = 1024*1024):
                f.write(chunk)
        f.close()
    logger.success("Done!\n")