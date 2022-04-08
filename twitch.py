import requests
import utils


class Twitch:
    def __init__(self):
        self.config = utils.read_config("config.json")
        self.bearer_token = None
        self.validate_bearer_token()
        self.logger = utils.Logger("TWITCH")

    def validate_bearer_token(self):
        if self.bearer_token:
            validate_url = "https://id.twitch.tv/oauth2/validate"
            headers = {
                "Authorization": f"Bearer {self.bearer_token}"
            }
            r = requests.get(validate_url, headers=headers).json()
            if "client_id" not in r:
                self.generate_bearer_token()
        else:
            self.generate_bearer_token()

    def generate_bearer_token(self):
        oauth_url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "grant_type": self.config["grant_type"]
        }
        r = requests.post(oauth_url, json=data).json()
        self.bearer_token = r["access_token"]

    def get_raw_url(self, slug):
        api_url = "https://api.twitch.tv/helix/clips"
        params = {
            "id": slug
        }
        headers = {
            "Client-ID": self.config["client_id"],
            "Authorization": f"Bearer {self.bearer_token}"
        }
        r = requests.get(api_url, params=params, headers=headers).json()
        if 'error' in r:
            if r["status"] == 500:
                print("Twitch is down")
        else:
            download_url = r["data"][0]["thumbnail_url"].split("-preview-")[0]
            return f"{download_url}.mp4"

    def download_video(self, url, output_path):
        self.logger.alert(f"\nDownloading {url} -> {output_path}")
        r = requests.get(url, stream=True)
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)
            f.close()
        self.logger.success("Done!\n")
