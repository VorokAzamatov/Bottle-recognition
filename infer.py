import click

from src.infer.pipeline import save_results
from src.infer.pipeline import run_comparison
from src.utils.init_config import init_config



@click.command()
@click.option('--use_config', '-cfg', type=bool,default=False, help="Use parameters from config file")
@click.option('--strip_width', '-sw', type=int, help="Strip width")
@click.option('--video_source', '-vp', help="Video source for match")
@click.option('--ref_frame_id', '-ri', help="Reference frame id ")
@click.option('--threshold', '-t', default=0.7, type=float, help="Minimum match threshold")
@click.option('--resize_factor', '-rf', default=1, type=float, help="Resize factor for size adjustment")
@click.option('--delay', '-d', default=30, type=int, help="Playback delay")

def main(use_config, video_source, ref_frame_id, strip_width, resize_factor, threshold, delay):
    frames_path = 'outputs/frames_output/frames.png'
    output_path = 'outputs/inference_outputs/infer_outputs.json'

    if use_config:
        config = init_config()

        video_source = config['general']['video_source']
        threshold = config['infer']['threshold'] 
        strip_width = config['infer']['strip_width']
        resize_factor = config['infer']['resize_factor'] 
        ref_frame_id = config['infer']['ref_frame_id'] 
        frames_path = config['general']['frames_path']
        output_path = config['infer']['output_path']

    else:
        print("Введите нужные параметры запуска или используйте параметры в 'configs/config.yaml' и значение '--use_config True'")
        print("Подробная информация по команде 'python scan.py --help'")
        return




    res_per_frame_dict, matched_frames_list = run_comparison(video_source, frames_path, resize_factor, ref_frame_id, strip_width, threshold, delay)


    if output_path:
        save_results(output_path, res_per_frame_dict, matched_frames_list)



if __name__ == '__main__':    
    main()