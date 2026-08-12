class Pizza:
    def __init__(self):
        self.dough = None
        self.sauce = None
        self.toppings = []

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()
        self.pizza.toppings = []

    def add_dough(self, dough):
        self.pizza.dough = dough
        return self

    def add_sauce(self, sauce):
        self.pizza.sauce = sauce
        return self

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self

    def get_pizza(self):
        return self.pizza