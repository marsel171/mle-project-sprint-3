# coding: utf-8
"""Класс FastApiHandler, который обрабатывает запросы API."""

import joblib
import numpy as np
from catboost import CatBoostRegressor


class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # Типы параметров запроса для проверки
        self.param_types = {"user_id": str, "model_params": dict}

        self.model_path = "./models/base_model"
        self.load_churn_model(model_path=self.model_path)

        # Необходимые параметры для предсказаний модели оттока
        self.required_model_params = [
            "building_id",
            "build_year",
            "building_type_int",
            "latitude",
            "longitude",
            "ceiling_height",
            "flats_count",
            "floors_total",
            "has_elevator",
            "floor",
            "kitchen_area",
            "living_area",
            "rooms",
            "is_apartment",
            "total_area",
        ]

    def load_churn_model(self, model_path: str):
        """Загружаем обученную модель
        Args:
            model_path (str): Путь до модели.
        """
        try:
            self.model = CatBoostRegressor()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def churn_predict(self, model_params: dict) -> float:
        """Предсказываем цену

        Args:
            model_params (dict): Параметры для модели.

        Returns:
            float - прогноз цены
        """
        param_values_list = list(model_params.values())
        return self.model.predict(param_values_list)

    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора параметров.

        Args:
            query_params (dict): Параметры запроса.

        Returns:
                bool: True - если есть нужные параметры, False - иначе
        """
        if "user_id" not in query_params or "model_params" not in query_params:
            return False

        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False

        if not isinstance(
            query_params["model_params"], self.param_types["model_params"]
        ):
            return False
        return True

    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора.

        Args:
            model_params (dict): Параметры пользователя для предсказания.

        Returns:
            bool: True - если есть нужные параметры, False - иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False

    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            - **dict**: Cловарь со всеми параметрами запроса.
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False

        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True

    def handle(self, params):
        """Функция для обработки запросов API параметров входящего запроса.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            - **dict**: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # Валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                user_id = params["user_id"]
                print(
                    f"Predicting for user_id: {user_id} and model_params:\n{model_params}"
                )
                # Получаем предсказания модели
                y_pred = self.churn_predict(model_params)
                response = {"user_id": user_id, "prediction": y_pred}
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response


if __name__ == "__main__":

    # Создаем тестовый запрос
    test_params = {
        "user_id": "123",
        "model_params": {
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
        },
    }

    # Создаем обработчик запросов для API
    handler = FastApiHandler()

    # Делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")
