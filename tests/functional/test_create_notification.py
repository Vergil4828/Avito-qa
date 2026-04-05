from typing import Any

import allure
import pytest

from helpers.base_test.base_test import BaseTest
from helpers.checkers.asserts import check_equal_length
from helpers.checkers.response_checker import check_status_code_http
from helpers.constants.base_constants import (
    BOOL_VALUES,
    ResponseStatusCodes,
    ErrorsMessages,
)
from helpers.constants.parametrizes import (
    FIELDS_CREATE_NOTIFICATIONS,
    NEGATIVE_NUMBER_IN_FIELDS_CREATE_NOTIFICATIONS,
    FIELDS_BIG_VALUE_CREATE_NOTIFICATIONS,
    STRING_FIELD_PARAMS,
)
from helpers.generic.functions import to_camel_case
from helpers.generic.random_helper import (
    get_rand_notification,
    gen_rand_int,
    gen_rand_str,
    gen_rand_float,
)
from utils.allure_marks import marks


@allure.epic("Тесты на создание объявлений")
@allure.description("Функциональные тесты, которые проверяют ручку создания объявления")
@allure.feature("POST /api/1/item")
class TestCreateNotification(BaseTest):
    @staticmethod
    def expected_message_json(notification_id: str):
        return {"status": f"Сохранили объявление - {notification_id}"}

    @staticmethod
    @allure.step("Проверяем ответ")
    def check_responses(
        responses: list,
        expected_status_code: int = ResponseStatusCodes.OK_STATUS_CODE.value,
        is_duplicate: bool = False,
        check_response_json: bool = False,
        expected_message: str = "",
    ):
        ids_set = set()
        for response in responses:
            with check_status_code_http(
                response=response,
                expected_response=(
                    TestCreateNotification.expected_message_json(
                        notification_id=response.data.get_id
                    )
                    if check_response_json
                    else None
                ),
                expected_status_code=expected_status_code,
                expected_message=expected_message,
            ):
                pass
            if response.status_code == ResponseStatusCodes.OK_STATUS_CODE.value:
                ids_set.add(response.data.get_id)
        with allure.step("Проверяем, что дубликаты имеют разные id"):
            if is_duplicate:
                check_equal_length(ids_set, responses)

    @staticmethod
    def get_json_struct(
        seller_id: Any = None,
        name: Any = None,
        price: Any = None,
        statistics_likes: Any = None,
        statistics_view_count: Any = None,
        statistics_contacts: Any = None,
    ):
        return {
            "sellerID": seller_id or gen_rand_int(),
            "name": name or gen_rand_str(),
            "price": price or gen_rand_int(),
            "statistics": {
                "likes": statistics_likes or gen_rand_int(),
                "viewCount": statistics_view_count or gen_rand_int(),
                "contacts": statistics_contacts or gen_rand_int(),
            },
        }

    @allure.title(
        "Проверяем успешное создание объявления со случайными данными. "
        "Также проверяем успешное создание дубликатов объявлений"
    )
    @marks.positive
    @pytest.mark.parametrize("is_duplicate", BOOL_VALUES)
    def test_create_notification(self, is_duplicate):
        template = get_rand_notification()
        notification_templates = [
            template for _ in range(gen_rand_int(2, 4) if is_duplicate else 1)
        ]
        with self.create_notifications(notification_templates) as responses:
            self.check_responses(
                responses, is_duplicate=is_duplicate, check_response_json=True
            )

    @allure.title(
        "Проверяем создание с отсутствующим полем или пустым/нулевым значением"
    )
    @marks.negative
    @pytest.mark.parametrize("field", FIELDS_CREATE_NOTIFICATIONS)
    @pytest.mark.parametrize("is_zero_int_or_str", BOOL_VALUES)
    def test_create_notification_with_empty_fields(self, field, is_zero_int_or_str):
        if field == "statistics":
            template = get_rand_notification()
            template.statistics = None
        else:
            template = get_rand_notification(
                **{
                    field: (
                        None if not is_zero_int_or_str else "" if field == "name" else 0
                    )
                }
            )
        error_field = (
            to_camel_case(field.replace("statistics_", "").replace("id", "ID"))
            if field != "statistics"
            else "likes"
        )
        with self.create_notifications([template]) as response:
            self.check_responses(
                response,
                expected_status_code=ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
                expected_message=ErrorsMessages.WRONG_REQUIRED_FIELD.format(
                    error_field
                ),
            )

    @allure.title(
        "Проверяем создание объявления с негативным значением в поле с типом int"
    )
    @marks.negative
    @pytest.mark.parametrize(
        "negative_field, status_code", NEGATIVE_NUMBER_IN_FIELDS_CREATE_NOTIFICATIONS
    )
    def test_create_notification_with_negative_numbers(
        self, negative_field, status_code
    ):
        with self.create_notifications(
            [get_rand_notification(**{negative_field: gen_rand_int(-(10**3), -1)})]
        ) as response:
            self.check_responses(response, expected_status_code=status_code)

    @allure.title(
        "Проверяем попытку создания объявления, когда в поля подаются не ожидаемые типы значений"
    )
    @marks.negative
    @pytest.mark.parametrize("field", FIELDS_CREATE_NOTIFICATIONS)
    def test_create_notification_with_invalid_value_in_field(self, field):
        if field != "statistics":
            values_for_int_field = [gen_rand_float(), gen_rand_str()]
            values_for_str_field = [gen_rand_int(), gen_rand_float()]
            for value in (
                values_for_str_field if field == "name" else values_for_int_field
            ):
                template = self.get_json_struct(**{field: value})
                with allure.step(
                    f"Пробуем создать объявление с полем {field}, которое имеет значение {value}"
                ):
                    with self.create_notifications([template]) as response:
                        self.check_responses(
                            response,
                            expected_status_code=ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
                            expected_message=ErrorsMessages.WRONG_EMPTY_VALUE.value,
                        )

    @allure.title("Проверяем создание объявления с большим значением в поле")
    @marks.negative
    @pytest.mark.parametrize("field", FIELDS_BIG_VALUE_CREATE_NOTIFICATIONS)
    def test_create_notification_with_big_value_in_field(self, field):
        template = self.get_json_struct(
            **{
                field: (
                    gen_rand_str(1) * gen_rand_int(10**4, 10**5)
                    if field == "name"
                    else gen_rand_int(10**20, 10**21)
                )
            }
        )
        with self.create_notifications([template]) as response:
            self.check_responses(
                response,
                expected_status_code=ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            )

    @allure.title("Проверяем создание объявления с разными значениями в поле name")
    @marks.negative
    @pytest.mark.parametrize("value, status_code", STRING_FIELD_PARAMS)
    def test_create_notification_with_check_name(self, value, status_code):
        with self.create_notifications([get_rand_notification(name=value)]) as response:
            self.check_responses(response, expected_status_code=status_code)
