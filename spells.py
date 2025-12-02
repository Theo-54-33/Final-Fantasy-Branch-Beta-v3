
class Spell:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description

FIRE = Spell("Fire", 8, "Strong single-target magic damage")
ICE = Spell("Ice", 10, "Damage + slow effect")
LIGHTNING = Spell("Lightning",12,"High damage, chance critical")
HEAL_ALL = Spell("Heal All",12,"Heals all allies")
POISON = Spell("Poison",10,"Applies poison damage over time")
