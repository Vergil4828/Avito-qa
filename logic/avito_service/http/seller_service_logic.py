from typing import Optional, Union

import allure

from clients.rest_client import RestClient
from models.http_models.base_model import ResponseModel
from models.http_models.seller_service_model import (
    CreateNotificationRequest,
    CreateNotificationResponse,
    GetNotificationByIdResponse,
    GetNotificationsBySellerIdResponse,
    GetStatisticsByIdResponse,
)


class SellerServiceLogic:
    """Основные ручки логики сервиса"""
    def __init__(self, client: RestClient):
        self.client = client

    @allure.step("Создаем объявление")
    def create_notification(self, request: Union[CreateNotificationRequest, dict]):
        response = self.client.post(endpoint="/api/1/item", json=request)
        return ResponseModel(response=response, model_class=CreateNotificationResponse)

    @allure.step("Получаем объявление по id")
    def get_notification_by_id(self, notification_id: str):
        response = self.client.get(endpoint=f"/api/1/item/{notification_id}")
        return ResponseModel(response=response, model_class=GetNotificationByIdResponse)

    @allure.step("Получаем объявления по seller_id")
    def get_notifications_by_seller_id(self, seller_id: int):
        response = self.client.get(endpoint=f"/api/1/{seller_id}/item")
        return ResponseModel(
            response=response, model_class=GetNotificationsBySellerIdResponse
        )

    @allure.step("Получаем cтатистику по id")
    def get_statistics_by_notification_id(self, notification_id: str):
        response = self.client.get(endpoint=f"/api/1/statistic/{notification_id}")
        return ResponseModel(response=response, model_class=GetStatisticsByIdResponse)

    @allure.step("Удаляем объявление")
    def delete_notification(self, notification_id: Optional[str]):
        return self.client.delete(endpoint=f"/api/2/item/{notification_id}")
