import pytest

from helpers.constants.base_constants import ResponseStatusCodes
from helpers.generic.functions import sort_list
from helpers.generic.random_helper import gen_rand_str

FIELDS_CREATE_NOTIFICATIONS = sort_list(
    [
        "seller_id",
        "name",
        "price",
        "statistics_likes",
        "statistics_view_count",
        "statistics_contacts",
        "statistics",
    ]
)

NEGATIVE_NUMBER_IN_FIELDS_CREATE_NOTIFICATIONS = sort_list(
    [
        pytest.param(
            "seller_id",
            ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            marks=pytest.mark.xfail(
                reason="ID автора объявления не может быть отрицательным"
            ),
        ),
        pytest.param(
            "price",
            ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            marks=pytest.mark.xfail(
                reason="Цена на объявление не может быть отрицательным"
            ),
        ),
        pytest.param(
            "statistics_contacts",
            ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            marks=pytest.mark.xfail(
                reason="Контакты объявления не могут быть отрицательными"
            ),
        ),
        pytest.param("statistics_likes", ResponseStatusCodes.OK_STATUS_CODE.value),
        pytest.param(
            "statistics_view_count",
            ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
            marks=pytest.mark.xfail(
                reason="Количество просмотров объявления не может быть отрицательным"
            ),
        ),
    ]
)

FIELDS_BIG_VALUE_CREATE_NOTIFICATIONS = sort_list(
    [
        pytest.param(
            "seller_id",
        ),
        pytest.param(
            "name",
            marks=pytest.mark.xfail(
                reason="Нельзя давать возможно создать название объявление со значением более 10 тысяч символов"
            ),
        ),
        pytest.param(
            "price",
        ),
        pytest.param(
            "statistics_likes",
        ),
        pytest.param(
            "statistics_view_count",
        ),
        pytest.param(
            "statistics_contacts",
        ),
    ]
)

STRING_FIELD_PARAMS = [
    pytest.param(
        f"  {gen_rand_str()}  ",
        ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
        marks=pytest.mark.xfail(
            reason="Нельзя создавать объявления с пробелами в начале/конце"
        ),
        id="Create_with_space",
    ),
    pytest.param(
        f"!@#$%^&*()_+ - {gen_rand_str()}",
        ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
        marks=pytest.mark.xfail(reason="Нельзя создавать объявления с спец символами"),
        id="Create_with_special_symbols",
    ),
    pytest.param(
        f"Кириллица - {gen_rand_str()}",
        ResponseStatusCodes.OK_STATUS_CODE.value,
        id="Create_with_cyrillic",
    ),
    pytest.param(
        "<script>alert(alert)</script>",
        ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
        marks=pytest.mark.xfail(
            reason="Нельзя позволять создавать объявление с xss скриптом"
        ),
        id="Create_with_xss_script",
    ),
    pytest.param(
        "'; DROP TABLE reasons;--",
        ResponseStatusCodes.BAD_REQUEST_STATUS_CODE.value,
        marks=pytest.mark.xfail(
            reason="Нельзя позволять создавать объявления с sql кодом"
        ),
        id="Create_with_sql_script",
    ),
]
