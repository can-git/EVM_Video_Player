import cv2
import numpy as np
import EVM

video_path = "results/video3_0.4_3_15.mp4"
low = 0.8
high = 2
amp = 10
video_name = video_path.split('/')[-1].split('.')[0]
video_amp_path = f"results/{video_name}_{low}_{high}_{amp}.mp4"


def draw_flow_arrows(image, flow, step=16, scale=1, min_length=8):
    h, w = image.shape[:2]
    y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x + fx * scale, y + fy * scale]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    for (x1, y1), (x2, y2) in lines:
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if length >= min_length:
            cv2.arrowedLine(image, (x1, y1), (x2, y2), (0, 255, 0), 1, tipLength=0.4)


# Load the video
cap = cv2.VideoCapture(video_path)
# cap = cv2.VideoCapture("results/amp_combined_edges_output.mp4")

# Take the first frame of the video
ret, first_frame = cap.read()
old_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# Set up the initial tracking point
height, width = first_frame.shape[:2]

# Create a mask image for drawing purposes
mask = np.zeros_like(first_frame)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("results/amp_combined_edges_output_flow.mp4", fourcc, 30, (width, height))

while True:
    # Read a new frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(old_gray, gray_frame, None, 0.5, 2, 15, 3, 5, 1.2, 0)

    # Draw arrows for optical flow vectors
    draw_flow_arrows(frame, flow)

    # Overlay the optical flow tracks on the original frame
    output = cv2.add(frame, mask)

    out.write(output)

    # Show the frame
    cv2.imshow('Tracking', output)

    # Update the previous frame and previous points
    first_frame = frame.copy()

    # Exit if ESC pressed
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
