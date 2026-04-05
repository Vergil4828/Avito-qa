from typing import TypeVar, Optional, Generic, Type

from pydantic import BaseModel, ConfigDict

T = TypeVar("T", bound=BaseModel)


class BaseModelApi(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class ResponseModel(Generic[T]):
    def __init__(self, response, model_class: Type[T] = None):
        self.status_code = response.status_code
        self.original_response = response
        self.data: Optional[T] = None

        if response.ok and model_class:
            self.data = model_class.model_validate(response.json())
