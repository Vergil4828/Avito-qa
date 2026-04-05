import contextlib
from typing import Union

import allure
import pytest

from helpers.checkers.response_checker import check_status_code_http
from helpers.constants.base_constants import NO_SET
from logic.avito_service import HTTPLogic
from models.http_models.base_model import ResponseModel
from models.http_models.seller_service_model import (
    Statistics,
    CreateNotificationRequest,
    CreateNotificationResponse,
)
from models.template_models.template_models import NotificationTemplate


@pytest.mark.usefixtures("setup_test_class")
class BaseTest(object):
    """
    Базовый класс для тестов, содержащий в себе логический модуль для обращения к ручкам различных сервисов.
    Также в классе содержатся вспомогательные функции
    """

    logic_helper: HTTPLogic = None

    @contextlib.contextmanager
    def create_notifications(
        self, notifications: list[Union[NotificationTemplate, dict]]
    ):
        responses: list[ResponseModel[CreateNotificationResponse]] = []
        try:
            for notification in notifications:
                if isinstance(notification, NotificationTemplate):
                    http_statistics = None
                    if (
                        notification.statistics is not NO_SET
                        and notification.statistics is not None
                    ):
                        http_statistics = Statistics(
                            likes=notification.statistics.likes,
                            viewCount=notification.statistics.view_count,
                            contacts=notification.statistics.contacts,
                        )
                    request = CreateNotificationRequest(
                        sellerID=notification.seller_id,
                        name=notification.name,
                        price=notification.price,
                        statistics=http_statistics,
                    )
                else:
                    request = notification
                responses.append(
                    self.logic_helper.avito_seller_service.create_notification(request)
                )
            yield responses
        finally:
            with allure.step("Удаляем новости"):
                for response in responses:
                    if response.data:
                        with check_status_code_http(
                            self.logic_helper.avito_seller_service.delete_notification(
                                response.data.get_id
                            )
                        ):
                            pass
