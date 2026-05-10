# Как работать с репозиторием
## Создайте папку проекта, например `sqllessons`
```
mrdir sqllessons
```
## Перейдите в созданную папку `sqllessons`
```
cd sqllessons
```
## Выполните комманду для клонирования репозитория в текущую директорию
```
git clone git@github.com:barmaley350/SQLLessons.git . 
```
## Создайте виртуальное окружение и установите необходимые зависимости в проект
```
uv sync
```
## Внесите изменения в `services/jupyter/examples.ipynb`
## Сгенерируйте новый файл `README.md`
```
uv run python3 main.py
```
## Запуск в docker и использование `jupeterlab` и `apache superset`


```
docker compose up --build
```
или
```
docker compose up
```

Jupyter доступен по url [http://localhost:8888/](http://localhost:8888/)

Apache Superset доступен по url [http://localhost:8088/](http://localhost:8088/)