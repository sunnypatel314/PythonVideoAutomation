import cv2
import random
import shutil
from moviepy.editor import *

class Video():
    def __init__(self, input_video_path, output_video_path, audio_file_path, desired_aspect_ratio=16/9):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.desired_aspect_ratio = desired_aspect_ratio
        self.audio_file_path = audio_file_path
    
    def extract_audio(self):
        audio = VideoFileClip(self.input_video_path).audio
        audio.write_audiofile(self.audio_file_path)

    def resize_video(self, new_height=480, new_width=540):
        print("Starting to resize clip...")
        # Open the video file

        # Open the input video
        cap = cv2.VideoCapture(self.input_video_path)

        # Get the original video's width, height, fps and codec
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4

        # Open the output video writer
        out = cv2.VideoWriter(self.output_video_path, fourcc, fps, (new_width, new_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize the frame
            resized_frame = cv2.resize(frame, (new_width, new_height))
            
            # Write the resized frame to the output video
            out.write(resized_frame)

        # Release resources
        cap.release()
        out.release()
        print("Video processing complete. Output saved to:", self.output_video_path)
        
    def inject_audio_into_video(self):
        audio_clip = AudioFileClip(self.audio_file_path)
        video_clip = VideoFileClip(self.output_video_path)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(f"results/{self.output_video_path[13:]}", codec="libx264", audio_codec='aac')

    def stack_with_gameplay(self, gameplay_file_path):
        clip = VideoFileClip(f"results/{self.output_video_path[13:]}")
        clip_duration = clip.duration
        gameplay = VideoFileClip(gameplay_file_path)
        gameplay_duration = gameplay.duration

        start_point = random.randint(0, int(gameplay_duration - clip_duration))
        end_point = int(clip_duration) + start_point

        gameplay_clip = gameplay.subclip(start_point, end_point)
        gameplay_clip = gameplay_clip.resize(width=clip.w)

        # Stack the clips vertically
        final_clip = clips_array([[clip], [gameplay_clip]])

        # os.remove(self.output_video_path)
        # Write the result to a file
        final_clip.write_videofile(self.output_video_path, codec="libx264")

    def remove_unwanted_files(self):
        os.remove(self.audio_file_path)
        os.remove(f"results/{self.output_video_path[13:]}")
        os.remove(self.input_video_path)