import cv2
import tkinter as tk
from tkinter import Button, Canvas, Label
from PIL import Image, ImageTk
import EVM
from os.path import exists
import click
import rearrange_video as rv


class VideoPlayer:
    def __init__(self, root, video_path, video_amp_path):
        self.root = root
        self.root.title("Video Player")

        video_path_normal = video_path
        video_path_amp = video_amp_path

        self.video_path_normal = video_path_normal
        self.video_path_amp = video_path_amp
        self.cap_normal = cv2.VideoCapture(self.video_path_normal)
        self.cap_amp = cv2.VideoCapture(self.video_path_amp)

        # Get video properties
        self.frame_rate = self.cap_normal.get(cv2.CAP_PROP_FPS)
        self.frame_delay = int(1000 / self.frame_rate)  # Delay in milliseconds

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the position of the window to be centered
        window_width = 640 * 2 + 50
        window_height = 600
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set window position
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.playing = False

        self.left_frame = tk.Frame(root, width=640, height=480)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.right_frame = tk.Frame(root, width=640, height=480)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

        self.bellow_frame = tk.Frame(root, width=640, height=30)
        self.bellow_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Create a canvas for the black box
        self.canvas = Canvas(self.left_frame, width=640, height=480, bg='black')
        self.canvas.pack()

        self.canvas_amp = Canvas(self.right_frame, width=640, height=480, bg='black')
        self.canvas_amp.pack()

        # Create control buttons
        self.play_button = Button(self.bellow_frame, text="Play", command=self.play_video)
        self.play_button.pack(side="left")

        self.pause_button = Button(self.bellow_frame, text="Pause", command=self.pause_video)
        self.pause_button.pack(side="left")

        self.replay_button = Button(self.bellow_frame, text="Replay", command=self.replay_video)
        self.replay_button.pack(side="left")

        self.frame_label = Label(self.bellow_frame, text="Frame: 0")
        self.frame_label.pack(side="right")

        self.update_frame()

    def play_video(self):
        self.playing = True
        # self.update_frame()

    def pause_video(self):
        self.playing = False

    def replay_video(self):
        self.cap_normal.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset the video to the beginning
        self.cap_amp.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset the video to the beginning
        self.playing = True
        # self.update_frame()

    def update_frame(self):
        if self.playing:
            ret, frame = self.cap_normal.read()
            ret_amp, frame_amp = self.cap_amp.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_amp = cv2.cvtColor(frame_amp, cv2.COLOR_BGR2RGB)

                img = Image.fromarray(frame)
                img_amp = Image.fromarray(frame_amp)
                imgtk = ImageTk.PhotoImage(image=img)
                imgtk_amp = ImageTk.PhotoImage(image=img_amp)

                self.canvas.create_image(320, 240, image=imgtk, anchor=tk.CENTER)  # Place image in the center
                self.canvas.imgtk = imgtk

                self.canvas_amp.create_image(320, 240, image=imgtk_amp, anchor=tk.CENTER)  # Place image in the center
                self.canvas_amp.imgtk = imgtk_amp

                current_frame = int(self.cap_normal.get(cv2.CAP_PROP_POS_FRAMES))
                self.frame_label.config(text=f"Frame: {current_frame}")

                # Delay based on frame rate
                self.root.after(self.frame_delay, self.update_frame)
            else:
                # Restart video if end is reached
                self.cap_normal.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.cap_amp.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.update_frame()
        else:
            # Check again after a short delay if paused
            self.root.after(100, self.update_frame)

    def __del__(self):
        if self.cap_normal.isOpened():
            self.cap_normal.release()


@click.command()
@click.option('--video_path', default='videos/video.mp4', help='Path to the input video file.')
@click.option('--low', default=0.4, type=float, help='Low frequency band for EVM.')
@click.option('--high', default=3, type=int, help='High frequency band for EVM.')
@click.option('--amp', default=10, type=int, help='Amplification factor for EVM.')
def run(video_path, low, high, amp):
    video_name = video_path.split('/')[-1].split('.')[0]
    video_amp_path = f"results/{video_name}_{low}_{high}_{amp}.mp4"

    if exists(video_amp_path) is False:
        print("Checking If the video is suitable for the pyramid")
        video_path = rv.make_video_divisible(video_path)

        print("AMP video is in the process, it will take a few minutes")
        EVM.magnify_motion(amp_video_path=video_amp_path, video_path=video_path, low=low, high=high, amplification=amp)

    root = tk.Tk()
    player = VideoPlayer(root, video_path, video_amp_path)
    root.mainloop()


if __name__ == "__main__":
    run()
