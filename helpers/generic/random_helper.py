import string
from random import randint, choice, uniform
from typing import Optional

from helpers.constants.base_constants import NO_SET
from helpers.generic.functions import add_field
from models.http_models.seller_service_model import Statistics
from models.template_models.template_models import NotificationTemplate


def gen_rand_int(a: int = 10**0, b: int = 10**5) -> int:
    return randint(a, b)


def gen_rand_str(length: int = 10) -> str:
    length = gen_rand_int(1, length)
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(length))


def gen_rand_float(a: int = 10**0, b: int = 10**5) -> float:
    return uniform(a, b)


def gen_rand_seller_id() -> int:
    return gen_rand_int(111_111, 10**6 - 1)


def get_rand_notification(
    seller_id: Optional[int] = NO_SET,
    name: Optional[str] = NO_SET,
    price: Optional[int] = NO_SET,
    statistics_likes: Optional[int] = NO_SET,
    statistics_view_count: Optional[int] = NO_SET,
    statistics_contacts: Optional[int] = NO_SET,
) -> NotificationTemplate:
    """Функция, возвращающая случайные данные для создания объявления"""
    return NotificationTemplate(
        seller_id=add_field(seller_id, gen_rand_seller_id()),
        name=add_field(name, gen_rand_str()),
        price=add_field(price, gen_rand_int()),
        statistics=Statistics(
            likes=add_field(statistics_likes, gen_rand_int()),
            viewCount=add_field(statistics_view_count, gen_rand_int()),
            contacts=add_field(statistics_contacts, gen_rand_int()),
        ),
    )
