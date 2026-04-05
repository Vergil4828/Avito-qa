from typing import Any

from assertpy import assert_that


def check_equal_length(actual: Any, expected: Any) -> Any:
    expected_length = expected if isinstance(expected, int) else len(expected)
    assert_that(actual, "Ожидаемые длины не совпадают").is_length(expected_length)
