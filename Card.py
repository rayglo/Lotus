class Card:

    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"Card ({self.value}, {self.color})"

    def __eq__(self, other):
        if other is None or not isinstance(other, Card):
            return False
        return self.value == other.value and self.color == other.color
