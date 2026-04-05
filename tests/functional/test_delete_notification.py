from typing import Optional

import allure
import pytest

from helpers.base_test.base_test import BaseTest
from helpers.checkers.response_checker import check_status_code_http
from helpers.constants.base_constants import (
    ResponseStatusCodes,
)
from helpers.generic.functions import to_json
from helpers.generic.random_helper import (
    get_rand_notification,
    gen_rand_str,
)
from models.http_models.base_model import ResponseModel
from utils.allure_marks import marks


@allure.epic("Тесты на удаление объявлений")
@allure.description("Функциональные тесты, которые проверяют ручку удаления объявлений")
@allure.feature("DELETE /api/2/item/:notification_id")
class TestDeleteNotification(BaseTest):

    @staticmethod
    @allure.step("Проверяем ответ")
    def check_response(
        response: ResponseModel,
        expected_status_code: int = ResponseStatusCodes.OK_STATUS_CODE.value,
        expected_response: Optional[dict] = None,
        expected_message: str = "",
    ):
        with check_status_code_http(
            response=response,
            expected_status_code=expected_status_code,
            expected_response=expected_response,
            expected_message=expected_message,
        ):
            return response

    @allure.title(
        "Проверяем, что созданное объявление имеет переданные поля по ручке получения объявления по id. "
        "Также проверяем, что дубликаты новостей имеют те же переданные поля, но уникальные id"
    )
    @marks.positive
    def test_delete_notification_by_id(self):
        template = get_rand_notification()
        response = self.check_response(
            response=self.logic_helper.avito_seller_service.create_notification(
                request=to_json(template)
            )
        )
        self.check_response(
            self.logic_helper.avito_seller_service.delete_notification(
                response.data.get_id
            )
        )

    @allure.title("Проверяем невозможность удалить объявление по неверному id")
    @marks.negative
    def test_delete_notification_by_id_with_invalid_id(self):
        self.check_response(
            self.logic_helper.avito_seller_service.delete_notification(gen_rand_str()),
            expected_status_code=ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
        )

    @allure.title("Проверяем, что удаленное объявление невозможно вновь удалить")
    @marks.negative
    @pytest.mark.e2e
    def test_delete_notification_by_id_after_delete_notification(self):
        with self.create_notifications([get_rand_notification()]) as response:
            pass
        self.check_response(
            response=self.logic_helper.avito_seller_service.delete_notification(
                notification_id=response[0].data.get_id
            ),
            expected_status_code=ResponseStatusCodes.NOT_FOUND_STATUS_CODE.value,
        )
