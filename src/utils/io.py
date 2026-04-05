import os
import json

def save_json(output_path, results):
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