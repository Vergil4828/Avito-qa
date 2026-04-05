import allure
import pytest


class Marks:
    @staticmethod
    def positive(func):
        allure.tag("positive")(func)
        return pytest.mark.positive(func)

    @staticmethod
    def negative(func):
        allure.tag("negative")(func)
        return pytest.mark.negative(func)


marks = Marks()
