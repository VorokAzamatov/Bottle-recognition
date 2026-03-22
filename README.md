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
    general:
    video_source: 'path/to/video.mp4'

    scan:
    strip_width: 130
    resize_factor: 0.5
    verbose: True
    vizualize: True

    infer:
    ref_frame_id: 74
    strip_width: 130
    resize_factor: 0.5
    threshold: 0.8
```