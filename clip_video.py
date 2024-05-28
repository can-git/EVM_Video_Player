from moviepy.editor import *

video_path = "videos/video.mp4"
clip = VideoFileClip(video_path)
clip = clip.subclip(0,20)


clip.write_videofile(video_path, codec='libx264')
