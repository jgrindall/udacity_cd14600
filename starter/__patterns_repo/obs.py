from typing import Optional
from abc import ABC, abstractmethod

class Observer(ABC):
    @property
    def logger(self):
        return self._logger

    def __init__(self, logger: Optional[object] = None):
        self._logger = logger

    @abstractmethod
    def update(self, message: str):
        pass



class Subject(ABC):
    def __init__(self):
        self._observers: list[Observer] = []

    def add(self, observer: Observer):
        self._observers.append(observer)

    def remove(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)


class Obs1(Observer):
    def update(self, message: str):
        if self._logger:
            self._logger.log(f"Obs1 received: {message}")


class Obs2(Observer):
    def update(self, message: str):
        if self._logger:
            self._logger.log(f"Obs2 received: {message}")


class Obs3(Observer):
    def update(self, message: str):
        if self._logger:
            self._logger.log(f"Obs3 received: {message}")
