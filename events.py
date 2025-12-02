
import random
def random_event(player):
    r = random.random()
    if r<0.1:
        gold = 20 + player.level*2
        player.gold += gold
        return f"Found a treasure chest! +{gold} gold"
    elif r<0.18:
        player.items['potion'] = player.items.get('potion',0)+1
        return "Found a potion!"
    elif r<0.22:
        player.hp = max(1, player.hp-10)
        return "You fell into a trap! Lost 10 HP"
    else:
        return None
