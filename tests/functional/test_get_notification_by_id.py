from typing import Optional

import allure
import pytest
from assertpy import assert_that

from helpers.base_test.base_test import BaseTest
from helpers.checkers.response_checker import check_status_code_http
from helpers.constants.base_constants import (
    ResponseStatusCodes,
    BOOL_VALUES,
    ErrorsMessages,
)
from helpers.generic.functions import to_json, TimeHelper
from helpers.generic.random_helper import (
    get_rand_notification,
    gen_rand_str,
    gen_rand_int,
)
from models.http_models.base_model import ResponseModel
from models.http_models.seller_service_model import GetNotificationByIdResponse
from utils.allure_marks import marks


@allure.epic("Тесты на получение объявлений")
@allure.description(
    "Функциональные тесты, которые проверяют ручку получения объявления по его id"
)
@allure.feature("GET /api/1/item/notification_id")
class TestGetNotificationById(BaseTest):

    @staticmethod
    @allure.step("Проверяем ответ")
    def check_response(
        response: ResponseModel[GetNotificationByIdResponse],
        expected_status_code: int = ResponseStatusCodes.OK_STATUS_CODE.value,
        expected_response: Optional[dict] = None,
        expected_message: str = "",
    ):
        if expected_response:
            expected_response["id"] = response.data.notification.id
        with check_status_code_http(
            response=response,
            expected_status_code=expected_status_code,
            expected_response=expected_response,
            ignore_list=["createdAt"],
            expected_message=expected_message,
        ):
            if expected_status_code == ResponseStatusCodes.OK_STATUS_CODE.value:
                with allure.step("Проверяем время создания объявления"):
                    assert_that(
                        TimeHelper.convert_time_str_to_timestamp(
                            response.data.notification.created_at
                        ),
                        "Время создания не совпадает с ожидаемым",
                    ).is_close_to(TimeHelper.get_current_timestamp(), tolerance=5)

    @allure.title(
        "Проверяем, что созданное объявление имеет переданные поля по ручке получения объявления по id. "
        "Также проверяем, что дубликаты новостей имеют те же переданные поля, но уникальные id"
    )
    @marks.positive
    @pytest.mark.parametrize("is_duplicate", BOOL_VALUES)
    def test_get_notification_by_id(self, is_duplicate):
        template = get_rand_notification()
        templates = [template for _ in range(gen_rand_int(2, 4))]
        with self.create_notifications(
            templates if is_duplicate else [template]
        ) as responses:
            for i, response in enumerate(responses):
                self.check_response(
                    response=self.logic_helper.avito_seller_service.get_notification_by_id(
                        notification_id=response.data.get_id
                    ),
                    expected_response=to_json(templates[i]),
                )

    @allure.title("Проверяем невозможность получить объявление по неверному id")
    @marks.negative
    def test_get_notification_by_id_with_invalid_id(self):
        notification_id = gen_rand_str()
        self.check_response(
            response=self.logic_helper.avito_seller_service.get_notification_by_id(
                notification_id=notification_id
            ),
            expected_status_code=ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            expected_message=ErrorsMessages.WRONG_ID_NOTIFICATION.format(
                notification_id
            ),
        )

    @allure.title("Проверяем, что удаленное объявление невозможно получить")
    @marks.negative
    @pytest.mark.e2e
    def test_get_notification_by_id_after_delete_notification(self):
        with self.create_notifications([get_rand_notification()]) as response:
            pass
        self.check_response(
            response=self.logic_helper.avito_seller_service.get_notification_by_id(
                notification_id=response[0].data.get_id
            ),
            expected_status_code=ResponseStatusCodes.NOT_FOUND_STATUS_CODE.value,
            expected_message=ErrorsMessages.WRONG_NOT_FOUND_NOTIFICATION.format(
                response[0].data.get_id
            ),
        )
