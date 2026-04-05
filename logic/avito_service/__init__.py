from functools import cached_property

from clients.rest_client import RestClient
from logic.avito_service.http.seller_service_logic import SellerServiceLogic


class HTTPLogic:
    """
    Основной класс для логики запросов к сервисам.
    Достаточно добавить в SERVICES в конфиге нужный сервис,
    прописать здесь добавление сервиса со своей логикой
    """
    def __init__(self, clients: dict[str, RestClient]):
        self._clients = clients

    @cached_property
    def avito_seller_service(self):
        return SellerServiceLogic(client=self._clients.get("avito_seller_service"))
