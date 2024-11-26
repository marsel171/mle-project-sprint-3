# Проект 3 спринта. 
## Цель проекта — вывести готовую модель для оценки цен на недвижимость в продакшен. 

### Имя бакета:
`s3-student-mle-20240919-f8666628fb`

### Микросервис для запуска ML-модели 

#### Этап 1. Написание FastAPI-микросервиса
 - Код микросервиса: 
 
    `./services/ml_service/churn_app.py`    

   ##### Микросервис принимает запросы и выдаёт предсказания модели в формате JSON `({"user_id": user_id, "prediction":y_pred})`, используя FastAPI и Uvicorn.

 - Класс-обработчик, который валидирует входные данные и возвращает предсказания:
 
   `./services/ml_service/fast_api_handler.py` 

 - Необходимые библиотеки: 
 
   `./services/requirements.txt`  

 - Пример запуска из директории `./services/`:

    ```bash
    uvicorn ml_service.churn_app:app --reload --port 1702 --host 0.0.0.0
    ```

 - Для просмотра документации API и совершения тестовых запросов зайти на: 
   
    `http://127.0.0.1:1702/docs`

#### Этап 2. Контейнеризация микросервиса
 - Dockerfile для сборки образа сервиса: 

   `./services/Dockerfile`

 - Переменные окружения, которые используются в Docker-контейнере:

   `./services/.env`

 - Инструкция по запуску: 

   - `docker image build . --tag price_predict:0`
   - `docker container run --publish 1702:1702 --volume=./models:/churn_app/models   --env-file .env price_predict:0`

 - Пример запроса для отработки микросервиса:
    ```bash
    curl -X 'POST' \
    'http://0.0.0.0:1702/api/churn/?user_id=123' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "building_id": 6220,
    "build_year": 1965,
    "building_type_int": 6,
    "latitude": 55.717113,
    "longitude": 37.78112,
    "ceiling_height": 2.64,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": 1,
    "floor": 9,
    "kitchen_area": 9.9,
    "living_area": 19.9,
    "rooms": 1,
    "is_apartment": 0,
    "total_area": 35.099998
    }'
    ```

#### Этап 3. Запуск сервисов для системы мониторинга
 - Файл для запуска сервиса в режиме Docker Compose c описанием сервисов
    - FastAPI
    - Prometheus
    - Grafana

   `./services/docker-compose.yaml`

 - Файл с микросервисом, в котором теперь присутствует запуск экспортера:

   `./services/ml_service/churn_app_prometheus.py`

 - Dockerfile для FastAPI-микросервиса c prometheus: 

   `./services/Dockerfile_prometheus`

 - Переменные окружения, которые используются в Docker-контейнере:

   `./services/.env`

- Cобственный конфиг Prometheus, который подключается в качестве тома в Docker:

   `./services/prometheus/prometheus.yml`
   
   ##### Базовые метрики, предоставляемые prometheus_fastapi_instrumentator, экспортируются на страницу /metrics.

 - Инструкция по запуску: 

   `docker compose up  --build`

  - Пример запроса для отработки микросервиса:
    ```bash
      curl -X 'POST' \
        'http://0.0.0.0:1702/api/churn/?user_id=123' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "building_id": 6220,
        "build_year": 1965,
        "building_type_int": 6,
        "latitude": 55.717113,
        "longitude": 37.78112,
        "ceiling_height": 2.64,
        "flats_count": 84,
        "floors_total": 12,
        "has_elevator": 1,
        "floor": 9,
        "kitchen_area": 9.9,
        "living_area": 19.9,
        "rooms": 1,
        "is_apartment": 0,
        "total_area": 35.099998
      }'
      ```

#### Этап 4. Построение дашборда для мониторинга
 - Скрипт, который симулирует нагрузку на сервис:

 `./services/test_requests.py`


 - Запуск скрипта в консоли:

  ```bash
  cd ./services/
  python test_requests.py
  ```

- Файл с дашбордом:

   `dashboard.json`

- Файл со скриншотом дашборда:

   `dashboard.png`