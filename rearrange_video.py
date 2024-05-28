from moviepy.editor import *

# loading video dsa gfg intro video
clip = VideoFileClip("videos/video_30.mp4")

# adding margin to the video
clip = clip.margin(top=2)
clip = clip.subclip(0, 20)

output_video_path = "videos/video_margin.mp4"
clip.write_videofile(output_video_path, codec='libx264')