import requests
import json
from moviepy.editor import VideoFileClip, concatenate_videoclips

with open('config.json') as f:
    config = json.load(f)
    client_id = config["client-id"]
    output_folder = config["out"]

def get_clip_data(slug):
    header = {
        "Client-ID": client_id,
        "Accept": "application/vnd.twitchtv.v5+json"
    }
    data = requests.get(f"https://api.twitch.tv/kraken/clips/{slug}", headers=header).json()
    url = data["thumbnails"]["medium"].split("-preview-")[0] + ".mp4"
    out_file = data["title"].replace(" ", "_") + ".mp4"
    return url, out_file

def download():
    path_array = []
    for clip in open("clips.txt", "r"):
        slug = clip.split("/")[5].strip("\n")
        url, out_filename = get_clip_data(slug)
        path = output_folder + out_filename
        print(f"\nDownloading {slug} -> {path}")
        r = requests.get(url, stream=True)
        with open(path, "wb") as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024):
                    f.write(chunk)
            f.close()
        print("Done!\n")
        path_array.append(path)
    return path_array

def main():
    clips = download()
    final = []
    for clip in clips:
        final.append(VideoFileClip(clip))
    concatenated = concatenate_videoclips(final)
    final_name = input("Name your file (include the .mp4 extension): ")
    concatenated.write_videofile(final_name)

if __name__ == "__main__":
    main()