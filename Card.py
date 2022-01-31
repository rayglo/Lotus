class Card:

    def __init__(self, color: str, value: int, age: int = 0):
        self.color = color
        self.value = value
        self.age = age

    def __str__(self):
        return f"Card ({self.value}, {self.color})"

    def __eq__(self, other):
        if other is None or not isinstance(other, Card):
            return False
        return self.value == other.value and self.color == other.color

    def increase_age(self):
        self.age += 1
