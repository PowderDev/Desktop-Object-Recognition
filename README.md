### Желательно скачать и установить CUDA.

[Ссылка на скачивание](https://developer.nvidia.com/cuda-11-7-1-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local)

В данном случае выбрана версия 11.7. Для работы с другими версиями нужно отредактировать ссылку в --index-url ниже

#### Запуск проекта

```bash
poetry install
poetry.exe run pip install torch torchvision --index-url https://download.pytorch.org/whl/cu117
poetry.exr run pip uninstall torch torchvision
poetry shell
python main.py
```

#### Модель

Посмотреть все модификации и их характеристики YOLOv8 можно [тут](https://github.com/ultralytics/ultralytics#models)

Переопределить можно изменив переменную YOLO_VERSION в main.py <br />
По умолчанию установлена YOLOv8s
