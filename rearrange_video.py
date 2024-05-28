from moviepy.editor import *


def is_divisible_by_2_three_times(value):
    for _ in range(3):
        if value % 2 != 0:
            return False
        value //= 2
    return True


def make_divisible_by_2_three_times(value):
    while not is_divisible_by_2_three_times(value):
        value += 1
    return value


def make_video_divisible(video_path):
    clip = VideoFileClip(video_path)
    new_h = 0
    new_w = 0

    if is_divisible_by_2_three_times(clip.h) is False:
        new_h = make_divisible_by_2_three_times(clip.h)
        clip = clip.margin(top=new_h - clip.h)
    if is_divisible_by_2_three_times(clip.w) is False:
        new_w = make_divisible_by_2_three_times(clip.w)
        clip = clip.margin(left=new_w - clip.w)

    if new_w != 0 or new_h != 0:
        clip.write_videofile(video_path, codec='libx264')
        print("Video is rearranged")
