"""Приложение Fast API для модели оценки цен на недвижимость."""


from fastapi import FastAPI, Body
from .fast_api_handler import FastApiHandler


# Создаем приложение Fast API
app = FastAPI()

# Создаем обработчик запросов для API
app.handler = FastApiHandler()


@app.post("/api/churn/")
def get_prediction_for_item(
    user_id: str,
    model_params: dict = Body(
        example={
            "building_id": 6220,
            "build_year": 1965,
            "building_type_int": 6,
            "latitude": 55.717113,
            "longitude": 37.781120,
            "ceiling_height": 2.64,
            "flats_count": 84,
            "floors_total": 12,
            "has_elevator": 1,
            "floor": 9,
            "kitchen_area": 9.9,
            "living_area": 19.900000,
            "rooms": 1,
            "is_apartment": 0,
            "total_area": 35.099998,
        }
    ),
):
    """Функция для получения предсказания цены.

    Args:
        user_id (str): Идентификатор пользователя.
        model_params (dict): Параметры объекта, которые мы должны подать в модель.

    Returns:
        dict: Предсказание цены на недвижимость.
    """
    all_params = {"user_id": user_id, "model_params": model_params}
    return app.handler.handle(all_params)
