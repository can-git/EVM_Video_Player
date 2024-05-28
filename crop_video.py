from moviepy.editor import *

video_path = "videos/video.mp4"
clip = VideoFileClip(video_path)
clip = clip.subclip(0,15)


clip.write_videofile("videos/video2.mp4")
