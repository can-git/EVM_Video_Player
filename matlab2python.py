import cv2
import numpy as np
import scipy.signal as signal
import scipy.fftpack as fftpack
import os

def build_gaussian_pyramid(src, level=3):
    s = src.copy()
    pyramid = [s]
    for i in range(level):
        s = cv2.pyrDown(s)
        pyramid.append(s)
    return pyramid


# Build Laplacian Pyramid
def build_laplacian_pyramid(src, levels=3):
    gaussianPyramid = build_gaussian_pyramid(src, levels)
    pyramid = []
    for i in range(levels, 0, -1):
        GE = cv2.pyrUp(gaussianPyramid[i])
        L = cv2.subtract(gaussianPyramid[i - 1], GE)
        pyramid.append(L)
    return pyramid



def reconstruct_laplacian_pyramid(pyramid):
    img = pyramid[0]
    for i in range(1, len(pyramid)):
        size = (pyramid[i].shape[1], pyramid[i].shape[0])
        img = cv2.pyrUp(img, dstsize=size)
        img = cv2.add(img, pyramid[i])
    return img


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    omega = 0.5 * fs
    low = lowcut / omega
    high = highcut / omega
    b, a = signal.butter(order, [low, high], btype='band')
    y = signal.lfilter(b, a, data, axis=0)
    return y

def save_video(amp_video_path, video_tensor_list):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    height, width = video_tensor_list[0].shape[0:2]
    writer = cv2.VideoWriter(amp_video_path, fourcc, 30, (width, height), True)

    for i in range(len(video_tensor_list)):
        a = cv2.convertScaleAbs(video_tensor_list[i])
        writer.write(a)

    writer.release()

def amplify_spatial_lpyr_temporal_iir(vidFile, resultsDir, alpha, lambda_c, r1, r2, chromAttenuation):
    vidName = os.path.splitext(os.path.basename(vidFile))[0]
    outName = os.path.join(resultsDir,
                           f"{vidName}.mp4")

    # Read video
    vid = cv2.VideoCapture(vidFile)
    fr = int(vid.get(cv2.CAP_PROP_FPS))
    vidWidth = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    vidHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_shape = (vidHeight, vidWidth)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vidOut = cv2.VideoWriter(outName, fourcc, fr, original_shape)

    # Define the number of levels for the Laplacian pyramid
    levels = 3

    ret, frame = vid.read()
    if not ret:
        raise ValueError("Error reading the video file.")
    frame = frame.astype('float')
    pyramid = build_laplacian_pyramid(frame, levels)

    lowpass1 = [pyr.copy() for pyr in pyramid]
    lowpass2 = [pyr.copy() for pyr in pyramid]
    frames = []
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break

        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame.astype('float')
        pyramid = build_laplacian_pyramid(frame, levels)

        # Temporal filtering
        # for l in range(len(pyramid)):
        #     lowpass1[l] = (1 - r1) * lowpass1[l] + r1 * pyramid[l]
        #     lowpass2[l] = (1 - r2) * lowpass2[l] + r2 * pyramid[l]
        #     pyramid[l] = (lowpass1[l] - lowpass2[l]) * alpha
        filter_tensor_list = []
        for i in range(levels):
            filter_tensor = butter_bandpass_filter(pyramid[i], 0.4, 3, 30)
            filter_tensor *= 10
            filter_tensor_list.append(filter_tensor)

        # Reconstruct the image from the modified pyramid
        output = reconstruct_laplacian_pyramid(pyramid)
        output = output.astype('float')

        # Normalize output to range 0-255 and convert to uint8
        output = cv2.normalize(output, None, 0, 255, cv2.NORM_MINMAX)
        # output = np.uint8(output)

        frames.append(output)

    vid.release()
    save_video(outName, frames)


# Usage example
amplify_spatial_lpyr_temporal_iir('videos/video4.mp4', 'results', 10, 16, 0.4, 0.05, 0.1)
