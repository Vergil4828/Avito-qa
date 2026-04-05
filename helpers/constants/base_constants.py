import enum

from helpers.generic.functions import sort_list

NO_SET = object()
BOOL_VALUES = sort_list([True, False])


class ResponseStatusCodes(enum.Enum):
    OK_STATUS_CODE = 200
    BAD_REQUEST_STATUS_CODE = 400
    NOT_FOUND_STATUS_CODE = 404


class ErrorsMessages(enum.Enum):
    WRONG_ID_NOTIFICATION = "ID айтема не UUID: {}"
    WRONG_SELLER_ID_NOTIFICATIONS = "передан некорректный идентификатор продавца"
    WRONG_STATISTICS_ID_NOTIFICATION = "передан некорректный идентификатор объявления"
    WRONG_REQUIRED_FIELD = "поле {} обязательно"
    WRONG_EMPTY_VALUE = "не передано тело объявления"
    WRONG_NOT_FOUND_NOTIFICATION = "item {} not found"

    def format(self, *args, **kwargs):
        return self.value.format(*args, **kwargs)
