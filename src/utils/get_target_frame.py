import cv2

def get_target_frame(frames_path, target_frame_id, strip_width):
    img = cv2.imread(frames_path)

    start = target_frame_id*strip_width
    end = start + strip_width

    target_frame = img[:, start:end]

    return target_frame