import cv2
import click
import numpy as np

import os

from src.utils.init_config import init_config
from src.img_processing.resize import resize
from src.img_processing.strip_frame import strip_frame



@click.command()
@click.option('--use_config', '-cfg', default=False, type=bool, help="Use parameters from config file")
@click.option('--strip_width', '-sw', type=int, help="Strip width")
@click.option('--video_source', '-vp', help="Video source for")
@click.option('--vizualize', '-vz', default=True, type=bool, help="Enable visualization")
@click.option('--resize_factor', '-rf', default=1, type=float, help="Resize factor for size adjustment")
@click.option('--verbose', '-vb', default=True, type=bool, help="Displaying information about the execution process")

def main(video_source, strip_width, use_config, resize_factor, vizualize, verbose):
    frames_path = 'outputs/frames_output/frames.png'

    if use_config:            
        config = init_config()
        
        verbose = config['scan']['verbose'] 
        vizualize = config['scan']['vizualize'] 
        strip_width = config['scan']['strip_width']
        video_source = config['general']['video_source']
        resize_factor = config['scan']['resize_factor'] 
        frames_path = config['general']['frames_path']
    else:
        print("Введите нужные параметры запуска или используйте параметры в 'configs/config.yaml' и значение '--use_config True'")
        print("Подробная информация по команде 'python scan.py --help'")
        return
    
    cap = cv2.VideoCapture(video_source)

    unwrapped_image = None
    frame_count = 0

    width, height = resize(cap, factor=resize_factor)
    output_dir = os.path.dirname(frames_path)

    while True:
        success, frame = cap.read()
        if not success:
            break


        frame = cv2.resize(frame, (width, height))
        stripped_frame = strip_frame(frame, strip_width)


        if unwrapped_image is None:
            unwrapped_image = stripped_frame
        else:
            unwrapped_image = np.hstack((unwrapped_image, stripped_frame))


        if vizualize:
            cv2.imshow('res', stripped_frame)

        if verbose:
            frame_count += 1
            if frame_count % 10 == 0:
                print(f"Обработано {frame_count} кадров...")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(frames_path, unwrapped_image)

    if os.path.exists(frames_path):
        print(f"Развертка успешно сохранена: {frames_path}")
    else:
        print(f"Развертка не была сохранена!: {frames_path}")



if __name__ == '__main__':    
    main()