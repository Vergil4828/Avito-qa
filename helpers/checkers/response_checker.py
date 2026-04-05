from contextlib import contextmanager
from typing import Optional, Union

import allure
from assertpy import assert_that

from helpers.constants.base_constants import ResponseStatusCodes
from models.http_models.base_model import ResponseModel


@allure.step("Проверяем, что ответ имеет ожидаемый статус код, ответ и ошибку")
@contextmanager
def check_status_code_http(
    response: ResponseModel,
    expected_status_code: int = ResponseStatusCodes.OK_STATUS_CODE.value,
    expected_message: str = "",
    expected_response: Optional[Union[dict, list[dict]]] = None,
    ignore_list: Optional[list] = None,
    check_all_in_list: bool = False,
):
    """Универсальный чекер response"""
    assert_that(
        response.status_code, "Код ответа не соответствует ожидаемому виду"
    ).is_equal_to(expected_status_code)
    if expected_message:
        assert_that(
            response.original_response.text, "Ответ не содержит ожидаемый текст"
        ).contains(expected_message)
    if expected_response:
        actual_response = response.original_response.json()
        if not check_all_in_list:
            actual_response = (
                [actual_response[0]]
                if isinstance(actual_response, list)
                else [actual_response]
            )
            expected_response = (
                [expected_response[0]]
                if isinstance(expected_response, list)
                else [expected_response]
            )
        for i, actual_json in enumerate(actual_response):
            assert_that(
                actual_json, "Ответ не соответствует ожидаемому виду"
            ).is_equal_to(expected_response[i], ignore=ignore_list)

    yield response
