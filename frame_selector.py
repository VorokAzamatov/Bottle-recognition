import cv2

import os

from src.utils.init_config import init_config
from src.utils.get_target_from_frames import get_target_from_frames


def main():
    config = init_config()
    target_frame_save_path = config['general']['target_frame_path']
    frames_img_path = config['general']['frames_path']
    strip_width = config['general']['strip_width']


    frames_img = cv2.imread(frames_img_path)

    frames_img_W = frames_img.shape[1]
    counter = int(frames_img_W / strip_width)
    
    frame_idx = 0
    while frame_idx < counter:
        print(f"frame_id: {frame_idx}")

        start = frame_idx * strip_width
        end = start + strip_width

        frame = frames_img[:, start:end]

        cv2.imshow("res", frame)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('n'):
            frame_idx += 1
        elif key == ord('p'):
            frame_idx -= 1
        elif key == ord(' '):
            target_frame = get_target_from_frames(frames_img_path, frame_idx, strip_width)

            print(f"Целевой кадр: {frame_idx}")

            cv2.imwrite(target_frame_save_path, target_frame)
            if os.path.exists(target_frame_save_path):
                print(f"Целевой кадр успешно сохранен: {target_frame_save_path}")
            else:
                print(f"Целевой кадр не был сохранен!: {target_frame_save_path}")
            
            print('Чтобы выйти нажмите "q"')

            

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()