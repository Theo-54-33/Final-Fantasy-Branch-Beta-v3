
class Item:
    def __init__(self, name, description, price=0):
        self.name = name
        self.description = description
        self.price = price

POTION = Item("Potion", "Restores HP", price=12)
ELIXIR = Item("Elixir", "Restores HP+MP", price=60)
ANTIDOTE = Item("Antidote", "Cures poison", price=15)
BOMB = Item("Bomb", "Damages all enemies", price=40)
