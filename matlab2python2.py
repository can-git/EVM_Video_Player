import cv2
import numpy as np
import os


def build_laplacian_pyramid(img, levels):
    pyramid = [img]
    for _ in range(levels):
        img = cv2.pyrDown(img)
        pyramid.append(img)
    laplacian_pyramid = [pyramid[-1]]
    for i in range(levels, 0, -1):
        size = (pyramid[i - 1].shape[1], pyramid[i - 1].shape[0])
        gaussian_expanded = cv2.pyrUp(pyramid[i], dstsize=size)
        laplacian = cv2.subtract(pyramid[i - 1], gaussian_expanded)
        laplacian_pyramid.append(laplacian)
    return laplacian_pyramid


def reconLpyr(filtered, pind):
    level = len(pind)
    pind = np.vstack([pind, [1, 1]])
    ind = np.cumsum(np.prod(pind, axis=1))
    ind = np.concatenate(([0], ind))
    for l in range(level - 1, -1, -1):
        filtered[ind[l]:ind[l + 1]] = filtered[ind[l]:ind[l + 1]] + \
                                      np.transpose(np.reshape(filtered[ind[l]:ind[l + 1]],
                                                              (pind[l][0], pind[l][1])), axes=(1, 0))
    return np.reshape(filtered[0:ind[1]], pind[0])


def amplify_spatial_lpyr_temporal_iir(vidFile, resultsDir, alpha, lambda_c, r1, r2, chromAttenuation):
    vidName = os.path.splitext(os.path.basename(vidFile))[0]
    outName = os.path.join(resultsDir, f"{vidName}-iir-r1-{r1}-r2-{r2}-alpha-{alpha}-lambda_c-{lambda_c}-chromAtn-{chromAttenuation}.avi")

    vid = cv2.VideoCapture(vidFile)
    fr = int(vid.get(cv2.CAP_PROP_FPS))
    vidWidth = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    vidHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    len = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    vidOut = cv2.VideoWriter(outName, cv2.VideoWriter_fourcc(*'XVID'), fr, (vidWidth, vidHeight))

    ret, frame = vid.read()
    if not ret:
        raise ValueError("Error reading the video file.")

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame.astype('float')
    pyramid = build_laplacian_pyramid(frame, 3)

    lowpass1 = [pyr.copy() for pyr in pyramid]
    lowpass2 = [pyr.copy() for pyr in pyramid]

    startIndex = 1
    endIndex = len - 10

    vidOut.write(cv2.cvtColor(np.uint8(frame), cv2.COLOR_RGB2BGR))

    for i in range(startIndex + 1, endIndex):
        ret, frame = vid.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.astype('float')
        pyramid = build_laplacian_pyramid(frame, 3)

        lowpass1 = [(1 - r1) * lp + r1 * pyr for lp, pyr in zip(lowpass1, pyramid)]
        lowpass2 = [(1 - r2) * lp + r2 * pyr for lp, pyr in zip(lowpass2, pyramid)]

        filtered = [lp1 - lp2 for lp1, lp2 in zip(lowpass1, lowpass2)]


        ind = 1080
        delta = lambda_c / 8 / (1 + alpha)
        exaggeration_factor = 2
        lambda_ = (vidHeight ** 2 + vidWidth ** 2) ** 0.5 / 3

        for l in range(len(pyramid) - 1, -1, -1):
            if l != 2 and l != 0:
                currAlpha = lambda_ / delta / 8 - 1
                currAlpha = currAlpha * exaggeration_factor
                if currAlpha > alpha:
                    filtered[ind] *= alpha
                else:
                    filtered[ind] *= currAlpha
            ind -= pyramid[l].shape[0] * pyramid[l].shape[1]

        output = np.zeros_like(frame)
        output[:, :, 0] = reconLpyr(filtered[:, :, 0], [pyr.shape for pyr in pyramid])
        output[:, :, 1] = reconLpyr(filtered[:, :, 1], [pyr.shape for pyr in pyramid])
        output[:, :, 2] = reconLpyr(filtered[:, :, 2], [pyr.shape for pyr in pyramid])

        output[:, :, 1] *= chromAttenuation
        output[:, :, 2] *= chromAttenuation

        output = output + frame
        output[output > 1] = 1
        output[output < 0] = 0

        output = (output * 255).astype(np.uint8)
        vidOut.write(cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

    vid.release()
    vidOut.release()


# Usage example
amplify_spatial_lpyr_temporal_iir('videos/video4.mp4', 'results', 10, 16, 0.4, 0.05, 0.1)
