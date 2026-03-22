import cv2

def resize(cap, factor):
    orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    new_width = int(orig_w * factor)
    new_height = int(orig_h * factor)

    return new_width, new_height