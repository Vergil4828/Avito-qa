import pytest
import requests

from clients.rest_client import RestClient
from configs.config import SERVICES
from configs.logging import configure_logging
from logic.avito_service import HTTPLogic


@pytest.fixture(scope="session", autouse=True)
def sessions():
    services_session = {}
    for service in SERVICES.get("http").values():
        services_session[service.name] = requests.Session()

    yield services_session

    for session in services_session.values():
        session.close()


@pytest.fixture(scope="session")
def clients(sessions):
    clients = {}
    for service_name, service_session in sessions.items():
        clients[service_name] = RestClient(
            session=service_session,
            url=SERVICES.get("http").get(service_name).url,
            name=SERVICES.get("http").get(service_name).name,
        )
    yield clients


@pytest.fixture(scope="class")
def setup_test_class(request, clients):
    if hasattr(request.cls, "logic_helper"):
        request.cls.logic_helper = HTTPLogic(clients)
    yield
    if hasattr(request.cls, "logic_helper"):
        request.cls.logic_helper = None


configure_logging()
