## N-граммная модель для генерации текстов
____
## Интерфейс:
    train.py --input-dir 'Путь к папке с текстами' --model 'Путь к сериализованной модели'
    generate.py --model 'Путь к сериализованной модели' --prefix 'Начало предложения' --length 'Длина выходного текста'