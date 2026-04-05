import click

from src.utils.io import save_json
from src.utils.plot import build_plot
from src.utils.init_config import init_config
from src.infer.pipeline import run_inference


@click.command()
@click.option('--use_config', '-cfg', type=bool, default=False, help="Use parameters from config file")
@click.option('--plot', '-p', default=True, type=bool, help="build a frame-by-frame match-score plot at the end")

def main(use_config, plot):
    output_path = 'outputs/inference_outputs/infer_outputs.json'

    if use_config:
        config = init_config()

        plot = config['infer']['plot']
        output_path = config['infer']['output_path']


    else:
        print("Введите нужные параметры запуска или используйте параметры в 'configs/config.yaml' и значение '--use_config True'")
        print("Подробная информация по команде 'python scan.py --help'")
        return


    results = run_inference(config)

    if output_path:
        save_json(output_path, results)
    
    if plot:
        build_plot()



if __name__ == '__main__':    
    main()