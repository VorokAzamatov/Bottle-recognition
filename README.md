# VideoStripper
Простой инструмент для развертки видео или прямой трансляции с веб-камеры в полосы кадров и сравнения с эталонным кадром.

## Установка

1.
```bash
    git clone https://github.com/VorokAzamatov/Bottle-recognition
```

2. 
```bash
    cd Bottle-recognition
    pip install -r requirements.txt
```



# Использование
### Сканирование видео
Параметры можно задавать вручную или определить все в файле `configs/config.yaml` и при запуске `--use_config True`
```bash
    python scan.py --video_source path/to/video.mp4 --strip_width 130 --resize_factor 0.5
```

### Запуск сравнения
```bash
    python infer.py --use_config True
```



### Горячие клавиши при визуализации
- q — выход
- space — пауза/воспроизведение
- n — следующий кадр
- p — предыдущий кадр




## Структура проекта
```
├─ src/
│   ├─ img_processing/       # функции обработки кадров
│   ├─ utils/                # вспомогательные функции
│   └─ infer/                # логика сравнения кадров
│
├─ outputs/                  # результаты
│   ├─ frames_output/
│   └─ inference_outputs/
│
├─ configs/
│   └─ config.yaml           # настройки проекта
│
├─ scan.py                   # скрипт развертки видео
├─ infer.py                  # скрипт сравнения кадров
└─ README.md
```


## Конфигурация

Настройки проекта хранятся в `configs/config.yaml`:
```YAML
    # === GENERAL ===
    general:
    video_source: 'videos/video.mp4'
    frames_path: 'outputs/frames_output/frames.png'
    target_frame_save_path: 'outputs/frames_output/target_frame.png'
    resize_factor: 0.35 # '1' not to use
    strip_width: 130

    # === SCAN ===
    scan:
    verbose: True
    vizualize: True


    # === INFERENCE ===
    infer:
    delay: 30
    plot: True
    threshold: 1
    roi_width: 200
    down_scale: 1 # '1' not to use
    steps_per_rev: 200
    output_path: 'outputs/inference_outputs/infer_outputs.json'
```