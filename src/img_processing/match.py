import cv2
import numpy as np



def match(reference, frame, threshold=0.8):
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(frame_gray, ref_gray, cv2.TM_CCOEFF_NORMED)

    max_val = np.max(result)

    return max_val >= threshold, max_val
