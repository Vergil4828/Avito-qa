import dataclasses
from typing import Optional

from helpers.constants.base_constants import NO_SET
from models.http_models.seller_service_model import Statistics


@dataclasses.dataclass
class NotificationTemplate:
    seller_id: Optional[int] = NO_SET
    name: Optional[str] = NO_SET
    price: Optional[int] = NO_SET
    statistics: Optional[Statistics] = NO_SET
