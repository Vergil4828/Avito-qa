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
    gen_rand_seller_id,
)
from models.http_models.base_model import ResponseModel
from models.http_models.seller_service_model import GetNotificationsBySellerIdResponse
from utils.allure_marks import marks


@allure.epic("Тесты на получение объявлений продавца")
@allure.description(
    "Функциональные тесты, которые проверяют ручку получения объявлений по seller_id"
)
@allure.feature("GET /api/1/:seller_id/item")
class TestGetNotificationsBySellerId(BaseTest):

    @staticmethod
    @allure.step("Проверяем ответ")
    def check_response(
        response: ResponseModel[GetNotificationsBySellerIdResponse],
        expected_status_code: int = ResponseStatusCodes.OK_STATUS_CODE.value,
        expected_response: Optional[list[dict]] = None,
        expected_message: str = "",
        check_all_in_list: bool = False,
    ):
        if expected_response:
            for i, elem_response in enumerate(response.data.root):
                expected_response[i]["id"] = elem_response.id
        with check_status_code_http(
            response=response,
            expected_status_code=expected_status_code,
            expected_response=expected_response,
            ignore_list=["createdAt"],
            expected_message=expected_message,
            check_all_in_list=check_all_in_list,
        ):
            if expected_status_code == ResponseStatusCodes.OK_STATUS_CODE.value:
                for elem_response in response.data.root:
                    with allure.step("Проверяем время создания объявления"):
                        assert_that(
                            TimeHelper.convert_time_str_to_timestamp(
                                elem_response.created_at
                            ),
                            "Время создания не совпадает с ожидаемым",
                        ).is_close_to(TimeHelper.get_current_timestamp(), tolerance=5)

    @allure.title(
        "Проверяем, что возвращаются все объявления у одного продавца. Также проверяем, что возвращаются дубликаты "
        "объявлений"
    )
    @marks.positive
    @pytest.mark.parametrize("is_duplicate_notifications", BOOL_VALUES)
    @pytest.mark.flaky(
        reruns=3,
        delay=0.5,
        reason="Тест может флакнуть из-за возможных старых данных от других тестировщиков",
    )
    def test_get_notifications_by_seller_id(self, is_duplicate_notifications):
        seller_id = gen_rand_seller_id()
        template = get_rand_notification(seller_id=seller_id)
        templates = [
            (
                template
                if is_duplicate_notifications
                else get_rand_notification(seller_id=seller_id)
            )
            for _ in range(gen_rand_int(2, 4))
        ]
        with self.create_notifications(templates):
            self.check_response(
                response=self.logic_helper.avito_seller_service.get_notifications_by_seller_id(
                    seller_id=seller_id
                ),
                expected_response=[to_json(template) for template in templates],
                check_all_in_list=True,
            )

    @allure.title(
        "Проверяем, что не находятся объявление у невалидного номера продавца"
    )
    @marks.negative
    def test_get_notifications_by_seller_id_with_invalid_id(self):
        seller_id = gen_rand_str()
        self.check_response(
            response=self.logic_helper.avito_seller_service.get_notifications_by_seller_id(
                seller_id=seller_id
            ),
            expected_status_code=ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            expected_message=ErrorsMessages.WRONG_SELLER_ID_NOTIFICATIONS.value,
        )

    @allure.title("Проверяем, что после удаления у продавца нет объявлений")
    @marks.negative
    @pytest.mark.e2e
    def test_get_notifications_by_seller_id_after_delete_notifications(self):
        seller_id = gen_rand_seller_id()
        with self.create_notifications(
            [
                get_rand_notification(seller_id=seller_id)
                for _ in range(gen_rand_int(2, 4))
            ]
        ):
            pass
        self.check_response(
            response=self.logic_helper.avito_seller_service.get_notifications_by_seller_id(
                seller_id=seller_id
            ),
            expected_status_code=ResponseStatusCodes.OK_STATUS_CODE.value,
            expected_response=[],
        )
