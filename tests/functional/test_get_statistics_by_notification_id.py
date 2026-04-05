from typing import Optional

import allure
import pytest

from helpers.base_test.base_test import BaseTest
from helpers.checkers.response_checker import check_status_code_http
from helpers.constants.base_constants import (
    ResponseStatusCodes,
    ErrorsMessages,
)
from helpers.generic.functions import to_json
from helpers.generic.random_helper import (
    get_rand_notification,
    gen_rand_str,
)
from models.http_models.base_model import ResponseModel
from models.http_models.seller_service_model import GetStatisticsByIdResponse
from utils.allure_marks import marks


@allure.epic("Тесты на получение статистики объявления")
@allure.description(
    "Функциональные тесты, которые проверяют ручку получения статистики объявление по его id"
)
@allure.feature("GET /api/1/statistic/:notification_id")
class TestGetStatisticsByNotificationId(BaseTest):

    @staticmethod
    @allure.step("Проверяем ответ")
    def check_response(
        response: ResponseModel[GetStatisticsByIdResponse],
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
            pass

    @allure.title("Проверяем, что можно получить статистику по созданному объявлению")
    @marks.positive
    def test_get_statistics_by_notification_id(self):
        template = get_rand_notification()
        with self.create_notifications([template]) as response:
            self.check_response(
                response=self.logic_helper.avito_seller_service.get_statistics_by_notification_id(
                    notification_id=response[0].data.get_id
                ),
                expected_response=to_json(template.statistics),
            )

    @allure.title(
        "Проверяем невозможность получить статистику по неверному id объявления"
    )
    @marks.negative
    def test_get_statistics_by_notification_id_with_invalid_notification_id(self):
        notification_id = gen_rand_str()
        self.check_response(
            response=self.logic_helper.avito_seller_service.get_statistics_by_notification_id(
                notification_id=notification_id
            ),
            expected_status_code=ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            expected_message=ErrorsMessages.WRONG_STATISTICS_ID_NOTIFICATION.value,
        )

    @allure.title(
        "Проверяем, что по удаленному объявлению невозможно получить статистику"
    )
    @pytest.mark.xfail(
        reason="По удаленном объявлению нельзя давать возможность получить статистику"
    )
    @pytest.mark.e2e
    @marks.negative
    def test_get_statistics_by_notification_id_after_delete_notification(self):
        with self.create_notifications([get_rand_notification()]) as response:
            pass
        self.check_response(
            response=self.logic_helper.avito_seller_service.get_statistics_by_notification_id(
                notification_id=response[0].data.get_id
            ),
            expected_status_code=ResponseStatusCodes.NOT_FOUND_STATUS_CODE.value,
        )
