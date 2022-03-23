import requests
import json
import os
import utils
import twitch
# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from moviepy.editor import VideoFileClip, concatenate_videoclips

def main(clips_filename):
    wrapper = twitch.Twitch()
    path_array = []
    for clip in open(clips_filename, "r"):
        slug = clip.split("/")[-1]
        download_dir = "_".join(clips_filename.split(".")[:-1])
        file_out = download_dir + "/" + slug + ".mp4"
        
        stream = wrapper.get_raw_url(slug)
        if stream:
            print(file_out)
            utils.download_video(stream, file_out)
            path_array.append(file_out)
    
    final = []
    for clip in path_array:
        final.append(VideoFileClip(clip))
    concatenated = concatenate_videoclips(final)
    final_name = input("Name your file (include the .mp4 extension): ")
    concatenated.write_videofile(final_name)

if __name__ == "__main__":
    main("clips.txt")