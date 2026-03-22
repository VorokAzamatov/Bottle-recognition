import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim

# Корреляция
def match(reference, frame, threshold=0.8):
    ref = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ref = ref.flatten()
    frm = frm.flatten()

    # нормализация
    ref = (ref - ref.mean()) / (ref.std() + 1e-6)
    frm = (frm - frm.mean()) / (frm.std() + 1e-6)

    score = np.dot(ref, frm) / len(ref)

    return score >= threshold, float(score)




# SSIM
# def match(reference, frame, threshold=0.75):
#     ref = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
#     frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     score = ssim(ref, frm)

#     return score >= threshold, float(score)




# # Градиенты
# def match(reference, frame, threshold=0.7):
#     ref = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
#     frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # градиенты
#     ref = cv2.Sobel(ref, cv2.CV_32F, 1, 0)
#     frm = cv2.Sobel(frm, cv2.CV_32F, 1, 0)

#     ref = ref.flatten()
#     frm = frm.flatten()

#     ref = (ref - ref.mean()) / (ref.std() + 1e-6)
#     frm = (frm - frm.mean()) / (frm.std() + 1e-6)

#     score = np.dot(ref, frm) / len(ref)

#     return score >= threshold, float(score)





# def match(reference, frame, threshold=0.8):
#     ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
#     frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     result = cv2.matchTemplate(frame_gray, ref_gray, cv2.TM_CCOEFF_NORMED)

#     max_val = np.max(result)

#     return max_val >= threshold, max_val


