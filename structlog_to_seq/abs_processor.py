from abc import ABCMeta, abstractmethod
from typing import Any


class AbsProcessor(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, logger, name, event_dict) -> Any:
        raise NotImplementedError
