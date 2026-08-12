from typing import Optional
from abc import ABC, abstractmethod

class ConcreteStrategy(ABC):
    def __init__(self, logger: Optional[object] = None):
        self._logger = logger

    @abstractmethod
    def execute(self, data: object):
        pass


class StrategyA(ConcreteStrategy):
    def execute(self, data: object):
        if self._logger:
            self._logger.log(f"Executing Strategy A with data: {data}")


class StrategyB(ConcreteStrategy):
    def execute(self, data: object):
        if self._logger:
            self._logger.log(f"Executing Strategy B with data: {data}")


class Processor:
    def __init__(self, strategy: ConcreteStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ConcreteStrategy):
        self._strategy = strategy

    def process(self, data: object):
        self._strategy.execute(data)