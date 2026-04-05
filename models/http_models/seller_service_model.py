"""Pydantic модели для сервиса"""
from typing import Optional

from pydantic import Field, RootModel

from helpers.constants.base_constants import NO_SET
from models.http_models.base_model import BaseModelApi


class Statistics(BaseModelApi):
    likes: Optional[int] = NO_SET
    view_count: Optional[int] = Field(default=NO_SET, alias="viewCount")
    contacts: Optional[int] = NO_SET


class CreateNotificationRequest(BaseModelApi):
    seller_id: Optional[int] = Field(alias="sellerID")
    name: Optional[str]
    price: Optional[int]
    statistics: Optional[Statistics]


class NotificationBase(CreateNotificationRequest):
    id: str
    seller_id: int = Field(alias="sellerId")
    created_at: str = Field(alias="createdAt")


class CreateNotificationResponse(BaseModelApi):
    status: str

    @property
    def get_id(self) -> str:
        return self.status.split(" - ")[-1]


class GetNotificationByIdRequest(BaseModelApi):
    id: str


class GetNotificationByIdResponse(RootModel[list[NotificationBase]]):

    @property
    def notification(self):
        return self.root[0]


class GetStatisticsByIdRequest(BaseModelApi):
    id: int


class GetStatisticsByIdResponse(RootModel[list[Statistics]]):
    pass


class GetNotificationsBySellerIdRequest(BaseModelApi):
    id: int


class GetNotificationsBySellerIdResponse(RootModel[list[NotificationBase]]):
    pass


class DeleteNotificationByIdRequest(BaseModelApi):
    id: Optional[str]


class DeleteNotificationByIdResponse(BaseModelApi):
    pass
