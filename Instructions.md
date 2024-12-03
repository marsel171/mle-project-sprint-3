# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-project-sprint-3

## 1. FastAPI микросервис в виртуальном окружение
```bash
cd ./services/
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt

# команда запуска сервиса с помощью uvicorn
uvicorn ml_service.churn_app:app --reload --port 1702 --host 0.0.0.0
```

### Пример curl-запроса к микросервису

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


## 2. FastAPI микросервис в Docker-контейнере

```bash
cd ./services/
docker image build . --tag price_predict:0
docker container run --publish 1702:1702 --volume=./models:/churn_app/models   --env-file .env price_predict:0
```

### Пример curl-запроса к микросервису

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

## 3. Docker compose для микросервиса и системы мониторинга

```bash
cd ./services/
docker compose up  --build
```

### Пример curl-запроса к микросервису

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

## 4. Скрипт симуляции нагрузки
Скрипт `test_requests.py` генерирует 100 запросов в течение 230 секунд.

```bash
# команды необходимые для запуска скрипта
cd ./services/
python test_requests.py
```

Адреса сервисов:
- микросервис: http://localhost:1702/
- Prometheus: http://localhost:9090/
- Grafana: http://localhost:3000/