import cv2

def convert_to_gray_and_trim(input_path, output_path, start_time, end_time):
    # Open the video file
    cap = cv2.VideoCapture(input_path)

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    print(f"Original video duration: {duration:.2f} seconds")

    # Calculate the start and end frames
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)

    current_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or current_frame > end_frame:
            break

        if current_frame >= start_frame:
            # Convert the frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Write the frame to the output video
            out.write(gray_frame)

        current_frame += 1

    # Release everything when done
    cap.release()
    out.release()
    print(f"Processed video saved as {output_path}")

# Example usage
convert_to_gray_and_trim('videos/video3.mp4', 'videos/video4.mp4', 0, 4)
