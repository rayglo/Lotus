import ConstantsGame


def color_allowed(color: str) -> bool:
    return color in ConstantsGame.colors


def value_allowed(value: int) -> bool:
    return value in ConstantsGame.values


def index_allowed(index: int) -> bool:
    return index < ConstantsGame.cards_per_hand
