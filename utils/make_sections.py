from moviepy.editor import *

def makeSections(video_source_file_path, count=1):
    # Load the video file
    video = VideoFileClip(video_source_file_path)

    video_duration = video.duration
    remainder = video_duration % 180

    sections = [[x, x+180] for x in range(0, int(video_duration)-180, 180)]
    sections.append([int(video_duration - remainder), int(video_duration)])
    if sections[-1][1] - sections[-1][0] < 60:
        sections.pop(-1)
        sections[-1][1] += int(remainder)
    sections = [tuple(s) for s in sections]

    total_clips_made = 0
    for i, (start, end) in enumerate(sections):
        if i > count - 1 and count != "max":
            break
        clip = video.subclip(start, end)
        clip.write_videofile(f"input_clips/section_{i+1}.mp4", codec="libx264")
        total_clips_made += 1
    
    return total_clips_made