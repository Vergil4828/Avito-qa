import os

from models.config_models.config_services_model import ConfigService

ADD_LOGS = os.getenv("ADD_LOGS", "True").lower() == "true"

SERVICES = {
    "http": {
        "avito_seller_service": ConfigService(
            name="avito_seller_service", url="https://qa-internship.avito.com"
        )
    }
}
