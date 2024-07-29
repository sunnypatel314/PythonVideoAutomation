from moviepy.editor import *

from utils.directories import makeDirectories, removeDirectories
from utils.make_sections import makeSections

from classes.Video import Video
from classes.Transcriber import Transriber

directories = ["input_clips", "output_clips", "audio", "results"]
makeDirectories(directories=directories)

count = 1
total_clips_made = makeSections("vids/episode_7.mp4", count=count) # for max, count="max"

list_of_video_objects = []

for i in range(total_clips_made):
    v = Video(input_video_path=f"input_clips/section_{i+1}.mp4", 
              output_video_path=f"output_clips/section_{i+1}.mp4", 
              audio_file_path=f"audio/section_{i+1}.wav")
    v.extract_audio()
    v.resize_video()
    v.inject_audio_into_video()
    list_of_video_objects.append(v)

print([v.output_video_path for v in list_of_video_objects])

for i in range(len(list_of_video_objects)):
    if not list_of_video_objects[i].audio_file_path:
        continue
    transcriber = Transriber(model_path="base", video_path=f"results/section_{i+1}.mp4", 
                             audio_path=list_of_video_objects[i].audio_file_path)
    transcriber.transcribe_video()
    transcriber.create_video()

for v in list_of_video_objects:
    v.stack_with_gameplay(gameplay_file_path=f"gameplay/subway_surfers.mp4")
    v.remove_unwanted_files()

directories_to_remove = ["audio", "input_clips", "results"]
removeDirectories(directories=directories_to_remove)