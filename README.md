# Общие схемы и модели

## Общие зависимости

- python3.11

- kafka:
```bash
docker run -p 9092:9092 --name kafka_dev apache/kafka:3.7.0
```

- postgres:
```bash
docker run -d --name postgres  --shm-size=1g -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres -c fsync=off
```


## Подготовка проекта

    git clone ____
    cd ____
    python -m venv venv
    source venv/bin/activate

В каждом сервисе:

    pip install -r requirements.txt
    cd -

Затем остальные requirements:

    pip install -r requirements.txt
    # Поставить локально общий пакет (если требуется его править и видеть результат до пуша в репозиторий):
    pip install -e ../api

Если Pycharm не видит установленную библиотеку api(grifon):
    
    File -> Settings -> Project -> Project Dependencies -> Выбрать текущий проект -> Поставить галочку на api

___

Архитектура проекта
![img.png](res/architecture.png)


## Дополнительные настройки и рекомендации

#### Создание миграций
    
    alembic revision --autogenerate -m "<describe change here>"

