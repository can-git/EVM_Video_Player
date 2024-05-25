# import cv2
# import numpy as np
# import scipy.signal as signal
# import scipy.fftpack as fftpack
# from tqdm import tqdm
# import tkinter as tk
# from tkinter import Scale, Button
# import EVM
#
# class VideoPlayerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Eulerian Video Magnification")
#
#         self.low_slider = Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", label="Low Frequency")
#         self.low_slider.set(0.4)
#         self.low_slider.pack()
#
#         self.high_slider = Scale(root, from_=1, to=10, orient="horizontal", label="High Frequency")
#         self.high_slider.set(3)
#         self.high_slider.pack()
#
#         self.amplification_slider = Scale(root, from_=1, to=30, orient="horizontal", label="Amplification")
#         self.amplification_slider.set(5)
#         self.amplification_slider.pack()
#
#         self.apply_button = Button(root, text="Apply", command=self.apply_magnification)
#         self.apply_button.pack()
#
#         self.video_name = "videos/video.mp4"
#
#     def apply_magnification(self):
#         low = self.low_slider.get()
#         high = self.high_slider.get()
#         amplification = self.amplification_slider.get()
#         self.magnify_motion(self.video_name, low, high, amplification)
#
#     def magnify_motion(self, video_name, low, high, levels=3, amplification=10):
#         t, f = EVM.load_video(video_name)  # frame ve fps
#         lap_video_list = EVM.laplacian_video(t, levels=levels)
#         filter_tensor_list = []
#         for i in range(levels):
#             filter_tensor = EVM.butter_bandpass_filter(lap_video_list[i], low, high, f)
#             filter_tensor *= amplification
#             filter_tensor_list.append(filter_tensor)
#         recon = EVM.reconstract_from_tensorlist(filter_tensor_list)
#         final = t + recon
#         EVM.save_video(final, low, high, amplification)
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VideoPlayerApp(root)
#     root.mainloop()