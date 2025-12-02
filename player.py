
import random
from config import PLAYER_BASE_HP, PLAYER_BASE_MP, PLAYER_BASE_ATK, PLAYER_BASE_MGC

class Player:
    def __init__(self, name="Hero"):
        self.name = name
        self.level = 1
        self.exp = 0
        self.next_exp = 30
        self.max_hp = PLAYER_BASE_HP
        self.hp = self.max_hp
        self.max_mp = PLAYER_BASE_MP
        self.mp = self.max_mp
        self.attack_power = PLAYER_BASE_ATK
        self.magic_power = PLAYER_BASE_MGC
        self.gold = 50
        self.items = {"potion": 2, "elixir": 0, "antidote": 0, "bomb":0}
        self.equipment = {}
    def attack(self, target):
        crit = random.random() < 0.1
        dmg = self.attack_power * (2 if crit else 1)
        target.take_damage(dmg)
        return int(dmg), crit
    def cast_fire(self, target):
        cost = 8
        if self.mp < cost:
            return None
        self.mp -= cost
        crit = random.random() < 0.08
        dmg = self.magic_power * 1.6 * (2 if crit else 1)
        target.take_damage(int(dmg))
        return int(dmg), crit
    def cast_ice(self, target):
        cost = 10
        if self.mp < cost:
            return None
        self.mp -= cost
        crit = random.random() < 0.06
        dmg = self.magic_power * 1.2 * (2 if crit else 1)
        target.take_damage(int(dmg))
        target.slowed = 1
        return int(dmg), crit
    def cast_lightning(self, target):
        cost = 12
        if self.mp < cost:
            return None
        self.mp -= cost
        dmg = self.magic_power * 2.0
        crit = random.random() < 0.05
        target.take_damage(int(dmg*(2 if crit else 1)))
        return int(dmg), crit
    def heal_self(self):
        cost = 6
        if self.mp < cost:
            return False,0
        self.mp -= cost
        amount = 30 + self.level*2
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return True, self.hp - old
    def use_item(self, item_name):
        if self.items.get(item_name,0) <= 0:
            return False,0
        if item_name == "potion":
            amount = 50 + self.level*3
            old = self.hp
            self.hp = min(self.max_hp, self.hp + amount)
            self.items[item_name] -= 1
            return True, self.hp - old
        if item_name == "elixir":
            oldhp = self.hp
            oldmp = self.mp
            self.hp = self.max_hp
            self.mp = self.max_mp
            self.items[item_name] -= 1
            return True, (self.hp-oldhp, self.mp-oldmp)
        if item_name == "antidote":
            # placeholder effect
            self.items[item_name] -= 1
            return True, "Cured poison"
        if item_name == "bomb":
            # damages all enemies handled externally
            self.items[item_name] -= 1
            return True, "Bomb used"
        return False,0
    def gain_exp(self, amount):
        self.exp += amount
        lvlups = 0
        messages = []
        while self.exp >= self.next_exp:
            self.exp -= self.next_exp
            self.level += 1
            lvlups += 1
            self.next_exp = int(self.next_exp * 1.4)
            self.max_hp += 12
            self.max_mp += 6
            self.attack_power += 3
            self.magic_power += 3
            self.hp = self.max_hp
            self.mp = self.max_mp
            messages.append(f"Level up to {self.level}!")
        return lvlups, messages
    def is_alive(self):
        return self.hp > 0
    def to_dict(self):
        return {"name":self.name,"level":self.level,"exp":self.exp,"next_exp":self.next_exp,
                "hp":self.hp,"mp":self.mp,"max_hp":self.max_hp,"max_mp":self.max_mp,
                "attack_power":self.attack_power,"magic_power":self.magic_power,
                "gold":self.gold,"items":self.items,"equipment":self.equipment}
    def take_damage(self, dmg):
        self.hp = max(0, self.hp - int(dmg))
