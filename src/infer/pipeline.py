import cv2

import os
import json

from src.img_processing.match import match
from src.img_processing.resize import resize
from src.img_processing.strip_frame import strip_frame
from src.utils.get_target_frame import get_target_frame



class FrameSource(object):
    def __init__(self, video_source, resize_factor):
        self.video_source = video_source
        self.resize_factor = resize_factor


        self.cap = cv2.VideoCapture(video_source)
        self.width, self.height = resize(self.cap, self.resize_factor)
        self.frames = []
        self.idx = 0

        self.live_mode = self._live_mode(video_source)
        if not self.live_mode:
            self._get_frames_from_vid(self.resize_factor)


    # -------------------------
    # internal
    # -------------------------
    def _get_frames_from_vid(self, resize_factor):
        self.frames = []

        while True:
            success, frame = self.cap.read()
            if not success:
                break
            frame_resized = cv2.resize(frame, (self.width, self.height))
            self.frames.append(frame_resized)

        self.cap.release()

    def _live_mode(self, video_source):
        frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

        if isinstance(video_source, int):
            return True

        if frame_count <= 0 or frame_count > 1e9:
            return True

        return False
            

    # -------------------------
    # public API
    # -------------------------
    def read(self):
        if self.live_mode:
            success, frame = self.cap.read()
            if not success:
                return False, None
            
            frame = cv2.resize(frame, (self.width, self.height))

            return True, frame
        else:
            if self.idx >= len(self.frames):
                return False, None

            frame = self.frames[self.idx]
            
            return True, frame
        
    def next(self):
        if not self.live_mode:
            self.idx += 1

    def prev(self):
        if not self.live_mode:
            self.idx = max(self.idx - 1, 0)



def vizualization(stripped_frame, frame_idx, matched, match_score):
    color = (0, 255, 0) if matched else (0, 0, 255)
    font_scale = 0.55
    border_thickness = 3
    text_thickness = 2

    vis = stripped_frame.copy()

    cv2.rectangle(vis, (0, 0), (vis.shape[1], vis.shape[0]), color, border_thickness)

    cv2.putText(vis, f"Frame: {frame_idx}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, text_thickness)
    cv2.putText(vis, f"Score: {match_score:.3f}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, text_thickness)

    cv2.imshow('Current frame', vis)


def save_results(output_path, res_per_frame_dict, matched_frames_list):
    return_dir = os.path.dirname(output_path)
    os.makedirs(return_dir, exist_ok=True)

    data = {
        'res_per_frame_dict': res_per_frame_dict, 
        'matched_frames_list': matched_frames_list 
    }
    with open(output_path, 'w') as f:
        json.dump(data, f)

    if os.path.exists(output_path):
        print(f"Результаты успешно сохранены: {output_path}")
    else:
        print(f"Результаты не были сохранены!: {output_path}")




def run_comparison(video_source, frames_path, resize_factor, ref_frame_id, strip_width, threshold, delay):
    target_frame = get_target_frame(frames_path, ref_frame_id, strip_width)
    target_frame_width = target_frame.shape[1]

    res_per_frame_dict = {}
    matched_frames_list = []

    source = FrameSource(video_source, resize_factor)

    frame_idx = 0
    paused = False
    while True:

        success, frame = source.read()
        if not success:
            break


        stripped_frame = strip_frame(frame, target_frame_width)

        matched, match_score = match(target_frame, stripped_frame, threshold=threshold)
        if matched:
            matched_frames_list.append(frame_idx)
        res_per_frame_dict[frame_idx] = {
            "matched": bool(matched),
            "score": float(match_score)
        }
        print(f"[Frame {frame_idx}] matched={matched} score={match_score:.4f}")
        

        vizualization(stripped_frame, frame_idx, matched, match_score)


        key = cv2.waitKey(delay if not paused else 0) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            paused = not paused
        elif key == ord('n'):
            source.next()
            frame_idx += 1
        elif key == ord('p'):
            source.prev()
            frame_idx -= 1
        elif not paused:
            source.next()
            frame_idx += 1

    source.cap.release()
    cv2.destroyAllWindows()

    return res_per_frame_dict, matched_frames_list