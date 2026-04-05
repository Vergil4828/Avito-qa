import dataclasses
import datetime
from typing import Any

from pydantic import BaseModel


def add_field(value: Any, generator_value: Any) -> Any:
    from helpers.constants.base_constants import NO_SET

    if value is NO_SET:
        return generator_value
    return value


def to_camel_case(string: str) -> str:
    elems = string.split("_")
    return elems[0] + "".join(x[0].upper() + x[1:] for x in elems[1:])


def to_json(obj) -> dict:
    from helpers.constants.base_constants import NO_SET

    if isinstance(obj, BaseModel):
        return obj.model_dump(by_alias=True, exclude_none=True)

    if dataclasses.is_dataclass(obj):
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            if value is not NO_SET:
                key = to_camel_case(field.name)
                result[key] = to_json(value)
        return result

    return obj


def sort_list(list_to_sort: list[Any]) -> list[Any]:
    return sorted(list_to_sort)


class TimeHelper:
    @staticmethod
    def get_current_datetime():
        return datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def convert_datetime_to_timestamp(date: datetime.datetime):
        return date.timestamp()

    @staticmethod
    def get_current_timestamp():
        return TimeHelper.convert_datetime_to_timestamp(
            TimeHelper.get_current_datetime()
        )

    @staticmethod
    def convert_time_str_to_timestamp(time_str: str):
        parts = time_str.split()
        clean_str_without_double_zone = f"{parts[0]} {parts[1]} {parts[2]}"
        return datetime.datetime.strptime(
            clean_str_without_double_zone, "%Y-%m-%d %H:%M:%S.%f %z"
        ).timestamp()
