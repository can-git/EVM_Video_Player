import cv2
import numpy as np


def detect_edges(input_path, output_path):
    # Open the video file
    cap = cv2.VideoCapture(input_path)

    # Get the frame rate and size of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)

    # Define the vertical and horizontal edge detection kernels
    kernel_vertical = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    kernel_horizontal = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply the Gaussian Blur to reduce noise
        blurred_frame = cv2.GaussianBlur(gray_frame, (7,7), 0)

        # Apply the custom vertical and horizontal edge detection kernels
        vertical_edges = cv2.filter2D(blurred_frame, -1, kernel_vertical)
        horizontal_edges = cv2.filter2D(blurred_frame, -1, kernel_horizontal)

        # Combine the edge maps by taking the magnitude of the gradients
        combined_edges = cv2.addWeighted(vertical_edges, 1, horizontal_edges, 1, 0)

        # Write the frame to the output video
        out.write(combined_edges)

        # Optionally display the frame
        cv2.imshow('Combined Edges', combined_edges)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
            break

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Processed video saved as {output_path}")


# Example usage
detect_edges('results/amp_combined_edges_output.mp4', 'results/amp_combined_edges_output2.mp4')
