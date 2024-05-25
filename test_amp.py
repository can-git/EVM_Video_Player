import cv2

import EVM
from tqdm import tqdm
import itertools


# lows = [0.1, 0.3, 0.4, 0.6, 0.8]
# highs = [2, 4, 6, 8, 10]
# amps = [5, 10, 15, 20, 30]

# combinations = list(itertools.product(lows, highs, amps))
# for low, high, amp in tqdm(combinations, desc="Processing", unit="step"):
#     # EVM.magnify_color("baby.mp4",0.4,3)
#     EVM.magnify_motion("videos/baby.mp4", low, high, amplification=amp)
#     break

EVM.magnify_motion("videos/baby.mp4", 0.4, 3, amplification=10)
