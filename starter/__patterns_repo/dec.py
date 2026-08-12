from typing import Optional
from abc import ABC, abstractmethod

class Drink(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def get_ingredients(self):
        pass


class SimpleCoffee(Drink):
    def get_name(self):
        return "Simple Coffee"

    def get_cost(self):
        return 2.0

    def get_ingredients(self):
        return ["Coffee"]


class Decorator(Drink):
    def __init__(self, drink: Drink):
        self._drink = drink

    def get_name(self):
        return self._drink.get_name()

    def get_cost(self):
        return self._drink.get_cost()

    def get_ingredients(self):
        return self._drink.get_ingredients()

class MilkDecorator(Decorator):
    def get_name(self):
        return self._drink.get_name() + " with Milk"

    def get_cost(self):
        return self._drink.get_cost() + 0.5

    def get_ingredients(self):
        return self._drink.get_ingredients() + ["Milk"]


class HotDecorator(Decorator):
    def get_name(self):
        return self._drink.get_name() + " (Hot)"

    def get_cost(self):
        return self._drink.get_cost() + 0.2

    def get_ingredients(self):
        return self._drink.get_ingredients() + ["Hot Water"]


        