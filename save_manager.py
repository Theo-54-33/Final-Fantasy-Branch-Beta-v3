
import json, os
from config import SAVE_FILE
def save(player, wave):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    data = {'player': player.to_dict(), 'wave': wave}
    with open(SAVE_FILE,'w',encoding='utf-8') as f:
        json.dump(data,f)
def load():
    import player as pmod
    if not os.path.exists(SAVE_FILE):
        return None,1
    with open(SAVE_FILE,'r',encoding='utf-8') as f:
        data = json.load(f)
    p = pmod.Player(data['player'].get('name','Hero'))
    p.level = data['player'].get('level',p.level)
    p.exp = data['player'].get('exp',p.exp)
    p.next_exp = data['player'].get('next_exp',p.next_exp)
    p.hp = data['player'].get('hp',p.hp)
    p.max_hp = data['player'].get('max_hp',p.max_hp)
    p.mp = data['player'].get('mp',p.mp)
    p.max_mp = data['player'].get('max_mp',p.max_mp)
    p.attack_power = data['player'].get('attack_power',p.attack_power)
    p.magic_power = data['player'].get('magic_power',p.magic_power)
    p.gold = data['player'].get('gold',p.gold)
    p.items = data['player'].get('items',p.items)
    return p, data.get('wave',1)
