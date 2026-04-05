import json
import uuid
from datetime import datetime
from typing import Optional, Union

import requests
import structlog
from pydantic import BaseModel

from configs.config import ADD_LOGS


class RestClient:
    """Основной клиент для использования методов"""

    def __init__(
        self,
        session: requests.Session,
        url: str,
        add_log: bool = ADD_LOGS,
        name: str = None,
    ):
        self.add_log = add_log
        self.url = url
        self.name = name
        if self.add_log:
            self.log = structlog.get_logger(self.__class__.__name__).bind(name=name)
        self.session = session

    def get(
        self, endpoint: str, params: Optional[BaseModel] = None, **kwargs
    ) -> requests.Response:
        return self._send_request(
            method="GET", endpoint=endpoint, params=params, **kwargs
        )

    def post(
        self, endpoint: str, json: Optional[Union[BaseModel, dict]] = None, **kwargs
    ) -> requests.Response:
        return self._send_request(method="POST", endpoint=endpoint, json=json, **kwargs)

    def put(
        self, endpoint: str, json: Optional[BaseModel] = None, **kwargs
    ) -> requests.Response:
        return self._send_request(method="PUT", endpoint=endpoint, json=json, **kwargs)

    def patch(
        self, endpoint: str, json: Optional[BaseModel] = None, **kwargs
    ) -> requests.Response:
        return self._send_request(
            method="PATCH", endpoint=endpoint, json=json, **kwargs
        )

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request(method="DELETE", endpoint=endpoint, **kwargs)

    def _send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        base_url = f"{self.url}{endpoint}"
        if kwargs.get("json") and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].model_dump(by_alias=True)
        if kwargs.get("params") and isinstance(kwargs["params"], BaseModel):
            kwargs["params"] = kwargs["params"].model_dump(by_alias=True)
        if kwargs.get("data") and isinstance(kwargs["data"], BaseModel):
            kwargs["data"] = kwargs["data"].model_dump(by_alias=True)
        if self.add_log:
            log = self.log.bind(request_id=str(uuid.uuid4()), name=self.name)
            log.info(
                "request",
                url=base_url,
                method=method,
                json=kwargs.get("json"),
                params=kwargs.get("params"),
                data=kwargs.get("data"),
                request_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            )
            response = self.session.request(method=method, url=base_url, **kwargs)
            response.encoding = "utf-8"
            log.info(
                "response",
                status_code=response.status_code,
                json=(
                    json.dumps(response.json(), indent=2, ensure_ascii=False)
                    if response.content
                    else "{}"
                ),
                text=response.text,
                duration=f"{response.elapsed.microseconds / 1000}ms",
                response_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            )
        else:
            response = self.session.request(method=method, url=base_url, **kwargs)
        return response
