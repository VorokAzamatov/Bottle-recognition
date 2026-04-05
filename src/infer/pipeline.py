import cv2

import os
import json

from src.img_processing.match import match
from src.img_processing.resize import resize
from src.img_processing.strip_frame import strip_frame



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
            self._get_frames_from_vid()


    # -------------------------
    # internal
    # -------------------------
    def _get_frames_from_vid(self):
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

    def release(self):
        self.cap.release()


def vizualization(frame, frame_idx, strip_width, results, show_strip):
    matched = results[frame_idx]['matched']


    color = (0, 255, 0) if matched else (0, 0, 255)
    font_scale = 0.55
    border_thickness = 3
    text_thickness = 2

    vis = frame.copy()

    cv2.rectangle(vis, (0, 0), (vis.shape[1], vis.shape[0]), color, border_thickness)


    for i, var_name in enumerate(['current_score', 'current_angle', 'target_angle', 'delta_angle', 'steps']):
        var_value = results[frame_idx][var_name]
        cv2.putText(vis, f"{var_name}: {var_value}", 
                    (10, (i+1)*25), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, text_thickness)
        
    if show_strip:
        h, w = vis.shape[:2]

        center_x = w // 2
        start_x = center_x - strip_width // 2
        end_x = center_x + strip_width // 2

        cv2.rectangle(
            vis,
            (start_x, 0),
            (end_x, h),
            (255, 255, 0), 
            2
        )

    cv2.imshow('Current frame', vis)


def save_results(output_path, results):
    return_dir = os.path.dirname(output_path)
    os.makedirs(return_dir, exist_ok=True)

    data = {
        'results': results
    }
    with open(output_path, 'w') as f:
        json.dump(data, f)

    if os.path.exists(output_path):
        print(f"Результаты успешно сохранены: {output_path}")
    else:
        print(f"Результаты не были сохранены!: {output_path}")


def angle_2_steps(angle, steps_per_rev):
    return int( round( angle * steps_per_rev / 360 ) )


def x_2_angle(x, frames_width):
    return (x / frames_width) * 360


def compute_delta_angle(current_angle, target_angle):
    delta = target_angle - current_angle

    if delta > 180:
        delta -= 360
    elif delta < -180:  
        delta += 360

    return delta


def find_position(frame, frames_gray, last_x=None, roi_width=200): 
    frames_width = frames_gray.shape[1]

    strip_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    if last_x is None:
        roi = frames_gray
        roi_offset = 0
    else:
        x_min = max(0, last_x - roi_width)
        x_max = min(frames_gray.shape[1], last_x + roi_width + strip_gray.shape[1])
        roi = frames_gray[:, x_min:x_max]
        roi_offset = x_min

    result = cv2.matchTemplate(roi, strip_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    x = max_loc[0] + roi_offset
    current_angle = x_2_angle(x, frames_width)

    return current_angle, x


def run_inference(config):
    target_frame_path = config['general']['target_frame_path']
    resize_factor = config['general']['resize_factor'] 
    video_source = config['general']['video_source']
    frames_path = config['general']['frames_path']
    strip_width = config['general']['strip_width']

    steps_per_rev = config['infer']['steps_per_rev']
    down_scale = config['infer']['down_scale']
    show_strip = config['infer']['show_strip']
    threshold = config['infer']['threshold'] 
    roi_width = config['infer']['roi_width']
    delay = config['infer']['delay']



    source = FrameSource(video_source, resize_factor)

    results = {}

    frames = cv2.imread(frames_path)
    frames = cv2.resize(frames, None, fx=down_scale, fy=down_scale)
    frames_gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY) 

    target_frame = cv2.imread(target_frame_path)
    target_frame = cv2.resize(target_frame, None, fx=down_scale, fy=down_scale)
    target_angle, _ = find_position(target_frame, frames_gray)

    last_x = None
    strip_width = int(strip_width * down_scale)

    frame_idx = 0
    paused = False
    while True:
        success, frame = source.read()
        if not success:
            break

        resized_frame = cv2.resize(frame, None, fx=down_scale, fy=down_scale)
        stripped_frame = strip_frame(resized_frame, strip_width)

        matched, current_score = match(target_frame, stripped_frame, threshold)

        current_angle, x = find_position(stripped_frame, frames_gray, last_x, roi_width)
        last_x = x

        delta_angle = compute_delta_angle(current_angle, target_angle)
        steps = angle_2_steps(delta_angle, steps_per_rev=steps_per_rev)


        results[frame_idx] = {
            'matched': 1 if matched else 0,
            'current_angle': round(current_angle, 4), 
            'current_score': round(current_score.item(), 4), 
            'target_angle': round(target_angle, 4), 
            'delta_angle': round(delta_angle, 4), 
            'threshold': threshold,
            'steps': steps
        }

        print(results[frame_idx])    
        vizualization(frame, frame_idx, strip_width, results, show_strip)

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

    source.release()
    cv2.destroyAllWindows()

    return results