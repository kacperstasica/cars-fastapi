import requests

from src.config import MODELS_FOR_MAKE_ENDPOINT


class CarExistenceChecker:
    def __init__(self, car_make, car_model):
        self.car_make = car_make
        self.car_model = car_model
        self.clean_car_make = None
        self.clean_car_model = None
        self.car_exists = False
        self.response = self.get_cars_response()
        self.check_model_for_make(self.response)

    def check_model_for_make(self, response):
        if not response:
            return
        if result := next(
            (
                item
                for item in response
                if item["Model_Name"].lower() == self.car_model.lower()
            ),
            None,
        ):

            self.car_exists = True
            self.clean_car_model = result["Model_Name"]
            self.clean_car_make = result["Make_Name"]

    def get_cars_response(self):
        response = requests.get(
            MODELS_FOR_MAKE_ENDPOINT.format(self.car_make),
        )
        if response_json := response.json().get("Results", None):
            return response_json
