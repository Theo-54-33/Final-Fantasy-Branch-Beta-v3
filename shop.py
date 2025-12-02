
from items import POTION, ELIXIR, ANTIDOTE, BOMB
class Shop:
    def __init__(self):
        self.inventory = {"potion": (POTION, 10), "elixir": (ELIXIR, 2), "antidote": (ANTIDOTE,5), "bomb": (BOMB,2)}
    def buy(self, player, key):
        if key not in self.inventory:
            return False,"Item not found"
        item, qty = self.inventory[key]
        if player.gold < item.price:
            return False,"Not enough gold"
        player.gold -= item.price
        player.items[key] = player.items.get(key,0) + 1
        return True,f"Bought {item.name}"
