import cv2
import numpy as np
import EVM

video_path = "videos/baby.mp4"
low = 0.4
high = 3
amp = 10
video_name = video_path.split('/')[-1].split('.')[0]
video_amp_path = f"results/{video_name}_{low}_{high}_{amp}.mp4"

# t, f = EVM.load_video(video_path)  # frame ve fps
# lap_video_list = EVM.laplacian_video(t, levels=3)
# filter_tensor_list = []
# for i in range(3):
#     filter_tensor = EVM.butter_bandpass_filter(lap_video_list[i], low, high, f)
#     filter_tensor *= amp
#     filter_tensor_list.append(filter_tensor)
# recon = EVM.reconstract_from_tensorlist(filter_tensor_list)
# EVM.save_video("deneme.mp4", recon)


# Load the video
cap = cv2.VideoCapture("deneme.mp4")
# cap = cv2.VideoCapture(video_amp_path)

# Take the first frame of the video
ret, first_frame = cap.read()

# Select a point to track
bbox = cv2.selectROI("Select point to track", first_frame, fromCenter=False, showCrosshair=True)
point = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))
cv2.destroyWindow("Select point to track")

# Set up the initial tracking point
old_points = np.array([[point]], dtype=np.float32)

# Create a mask image for drawing purposes
mask = np.zeros_like(first_frame)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

while True:
    # Read a new frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    new_points, status, error = cv2.calcOpticalFlowPyrLK(gray_first_frame, gray_frame, old_points, None, **lk_params)
    print(new_points)
    # Select good points
    good_new = new_points[status == 1]
    good_old = old_points[status == 1]

    # Draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        a = int(round(a))
        b = int(round(b))
        c = int(round(c))
        d = int(round(d))
        mask = cv2.line(mask, (a, b), (c, d), (0, 255, 0), 2)
        frame = cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)

    # Overlay the optical flow tracks on the original frame
    output = cv2.add(frame, mask)

    # Show the frame
    cv2.imshow('Tracking', output)

    # Update the previous frame and previous points
    first_frame = frame.copy()
    # old_points = good_new.reshape(-1, 1, 2)

    # Exit if ESC pressed
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


# EVM.magnify_motion(video_amp_path, "videos/baby.mp4", 0.4, 3, amplification=10)
