import cv2

from src.utils.init_config import init_config


def main():
    config = init_config()
    frames_img_path = config['general']['frames_path']
    strip_width = config['infer']['strip_width']


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

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()