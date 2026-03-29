import matplotlib.pyplot as plt

import json

from src.utils.init_config import init_config




def build_plot(grid=True):
    config = init_config()
    output_path = config['infer']['output_path']


    with open(output_path, 'rb') as file:
        data = json.load(file)

    current_score = [ dict['current_score'] for _, dict in data['results'].items() ]
    current_angle = [ dict['current_angle'] for _, dict in data['results'].items() ]
    delta_angle = [ dict['delta_angle'] for _, dict in data['results'].items() ]
    steps = [ dict['steps'] for _, dict in data['results'].items() ]


    plt.figure(figsize=(12, 8))

    plt.subplot(221)
    plt.title('current_score per frame')
    plt.plot(current_score)
    plt.grid(grid)

    plt.subplot(222)
    plt.title('current_angle per frame')
    plt.plot(current_angle)
    plt.grid(grid)

    plt.subplot(223)
    plt.title('delta_angle per frame')
    plt.plot(delta_angle)
    plt.grid(grid)

    plt.subplot(224)
    plt.title('steps per frame')
    plt.plot(steps)
    plt.grid(grid)

    plt.tight_layout()
    plt.show()
