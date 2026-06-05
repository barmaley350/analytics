# Описание
## Краткое описание
Приводится пример анализа данных на основе датасетов 

| Dataset | Размер файла | Кол-во строк | Кол-во столбцов | Описание |
|---------|---------|-----------|---------------|---------------|
|[Kaggle](https://www.kaggle.com/datasets/ekibee/car-sales-information) | `2.0G` | `1 294 757` | `19`| Продажа автомобилей в России |
|[Kaggle](https://www.kaggle.com/datasets/residentmario/iowa-liquor-sales) | `4.5G` | `19 666 763` | `24`| Продажа спиртных напитков в Айове |
## Общая схема работы
![png](files/md/main.png?1)

## Используемые инструменты

| Этап | Сервис | Url | Описание | 
|---------|---------|-----------|---------------|
| `подготовка` | python3, clickhouse-local |  | |
| `data profilling` `визуализация`| JupyterLab | [http://localhost:8888/](http://localhost:8888/) | `Data profiling` — это процесс исследования и анализа наборов данных для понимания их структуры, содержания и качества. Цель — получить полное представление о данных перед их использованием в анализе, машинном обучении или интеграции.  |
| `визуализация` | Apache Superset | [http://localhost:8088/](http://localhost:8088/) | `Apache Superset` — это бесплатная (open‑source) платформа для исследования и визуализации данных с веб‑интерфейсом. Изначально разработана в Airbnb, затем передана в Apache Software Foundation. |
| `хранение` | ClickHouse | [http://localhost:8123/](http://localhost:8123/) | `ClickHouse` — это колоночная (столбцовая) система управления базами данных (СУБД) с открытым исходным кодом (Apache License 2.0), разработанная в Яндексе для аналитики больших объёмов данных в реальном времени. |
| `хранение` | PostgreSQL | [http://localhost:5423/](http://localhost:5423/) |  |
| `визуализация` | PostgreSQL | [http://localhost:5000/](http://localhost:5000/) | `smtp4dev` — это бесплатный open‑source‑инструмент (под лицензией Apache 2.0), эмулирующий SMTP‑сервер для тестирования и отладки отправки писем в процессе разработки.  |

## Потребление ресурсов 
```
docker stats --no-stream $(docker ps --filter "name=sqllessons2" --format "{{.Names}}") --format "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.BlockIO}}|{{.NetIO}}" | awk 'BEGIN {print "| CONTAINER NAME | CPU % | MEM USAGE | MEM % | BLOCK I/O | NET I/O |"; print "|-|-|-|-|-|-|"} {print "| " $0 " |"}' | xclip -sel clip 
```
| CONTAINER NAME | CPU % | MEM USAGE | MEM % | BLOCK I/O | NET I/O |
|-|-|-|-|-|-|
| sqllessons2-service.superset_worker-1|0.24%|443.7MiB / 3.819GiB|11.34%|36.5MB / 12.3kB|861kB / 909kB |
| sqllessons2-service.superset_beat-1|0.00%|239.3MiB / 3.819GiB|6.12%|28.2MB / 0B|14.1kB / 8.53kB |
| sqllessons2-service.jupyter-1|0.09%|81.03MiB / 3.819GiB|2.07%|46.5MB / 1.4MB|1.9kB / 126B |
| sqllessons2-service.superset-1|0.05%|255.1MiB / 3.819GiB|6.52%|96.8MB / 0B|11.3kB / 6.07kB |
| sqllessons2-service.db_postgres-1|0.01%|43.73MiB / 3.819GiB|1.12%|17.1MB / 12.3kB|24.7kB / 34.6kB |
| sqllessons2-service.db_clickhouse-1|9.70%|897.7MiB / 3.819GiB|22.95%|529MB / 439MB|1.99kB / 126B |
| sqllessons2-service.redis-1|0.96%|9.098MiB / 3.819GiB|0.23%|3.66MB / 0B|902kB / 847kB |
| sqllessons2-service.smtp4dev-1|0.08%|73.44MiB / 3.819GiB|1.88%|48.8MB / 32.8kB|2.03kB / 126B |



## Как запустить
`docker compose  up --build`