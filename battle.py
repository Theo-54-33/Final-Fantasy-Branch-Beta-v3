
import pygame, sys, random, json, os
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, SAVE_FILE
from player import Player
from enemy import Enemy

def draw_text(surf, txt, x, y, size=20, color=(255,255,255)):
    font = pygame.font.SysFont(None, size)
    surf.blit(font.render(txt, True, color), (x,y))

def save_game(player, wave):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    data = {"player": player.to_dict(), "wave": wave}
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None, 1
    with open(SAVE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    p = Player(data['player'].get('name','Hero'))
    p.level = data['player'].get('level', p.level)
    p.exp = data['player'].get('exp', p.exp)
    p.next_exp = data['player'].get('next_exp', p.next_exp)
    p.max_hp = data['player'].get('max_hp', p.max_hp)
    p.hp = data['player'].get('hp', p.hp)
    p.max_mp = data['player'].get('max_mp', p.max_mp)
    p.mp = data['player'].get('mp', p.mp)
    p.attack_power = data['player'].get('attack_power', p.attack_power)
    p.magic_power = data['player'].get('magic_power', p.magic_power)
    p.gold = data['player'].get('gold', p.gold)
    p.items = data['player'].get('items', p.items)
    return p, data.get('wave',1)

def make_wave(wave):
    enemies = []
    # boss every 7 waves (endgame boss at wave 21)
    if wave % 7 == 0:
        hp = 160 + wave*30
        atk = 18 + wave//2
        enemies.append(Enemy("ENDGAME BOSS" if wave>=21 else "BOSS", hp, atk, special="boss", exp=80+wave*6, gold=80+wave*8))
        return enemies
    # otherwise mix of enemies
    count = min(3, 1 + wave//4)
    for i in range(count):
        hp = 50 + wave*10 + random.randint(-8,12)
        atk = 7 + wave//3
        special = "frenzy" if random.random() < 0.12 and wave>3 else None
        exp = 10 + wave*3
        gold = 8 + wave*4
        enemies.append(Enemy(f"Enemy{len(enemies)+1}", hp, atk, special=special, exp=exp, gold=gold))
    return enemies

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Final Fantasy Branch Beta - Battle")
    clock = pygame.time.Clock()
    player, start_wave = load_game()
    if not player:
        from player import Player as P
        player = P()
        start_wave = 1
    wave = start_wave
    enemies = make_wave(wave)
    turn = "player"
    selected_enemy = 0
    message = "Wave %d - Good luck!" % wave
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(player, wave)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and turn == 'player':
                mx,my = event.pos
                # buttons
                if 40<=mx<=200 and 520<=my<=590:
                    dmg, crit = player.attack(enemies[selected_enemy])
                    message = f"You attacked {enemies[selected_enemy].name} for {dmg} dmg{' (CRIT)' if crit else ''}"
                    turn = 'enemy'
                if 230<=mx<=390 and 520<=my<=590:
                    res = player.cast_fire(enemies[selected_enemy])
                    if res is None:
                        message = "Not enough MP!"
                    else:
                        dmg, crit = res
                        message = f"Fire hit {enemies[selected_enemy].name} for {dmg} dmg{' (CRIT)' if crit else ''}"
                        turn = 'enemy'
                if 420<=mx<=580 and 520<=my<=590:
                    res = player.cast_ice(enemies[selected_enemy])
                    if res is None:
                        message = "Not enough MP!"
                    else:
                        dmg, crit = res
                        message = f"Ice hit {enemies[selected_enemy].name} for {dmg} dmg{' (CRIT)' if crit else ''} (slowed)"
                        turn = 'enemy'
                if 610<=mx<=770 and 520<=my<=590:
                    ok, amt = player.heal_self()
                    if ok:
                        message = f"You healed for {amt} HP."
                        turn = 'enemy'
                    else:
                        message = "Not enough MP."
                if 800<=mx<=880 and 520<=my<=590:
                    ok, amt = player.use_item('potion')
                    if ok:
                        message = f"Used Potion: restored {amt} HP."
                        turn = 'enemy'
                    else:
                        message = "No potions left."
                # select enemy
                for idx,e in enumerate(enemies):
                    ex = 80 + idx*260
                    ey = 120
                    if ex<=mx<=ex+140 and ey<=my<=ey+140:
                        selected_enemy = idx
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and turn == 'player':
                    dmg, crit = player.attack(enemies[selected_enemy])
                    message = f"You attacked {enemies[selected_enemy].name} for {dmg} dmg{' (CRIT)' if crit else ''}"
                    turn = 'enemy'
                if event.key == pygame.K_f and turn == 'player':
                    res = player.cast_fire(enemies[selected_enemy])
                    if res is None:
                        message = "Not enough MP!"
                    else:
                        dmg,crit = res
                        message = f"Fire hit {enemies[selected_enemy].name} for {dmg} dmg"
                        turn = 'enemy'
                if event.key == pygame.K_i and turn == 'player':
                    res = player.cast_ice(enemies[selected_enemy])
                    if res is None:
                        message = "Not enough MP!"
                    else:
                        dmg,crit = res
                        message = f"Ice hit {enemies[selected_enemy].name} for {dmg} dmg (slowed)"
                        turn = 'enemy'
                if event.key == pygame.K_h and turn == 'player':
                    ok, amt = player.heal_self()
                    if ok:
                        message = f"You healed for {amt} HP."
                        turn = 'enemy'
                    else:
                        message = "Not enough MP."
                if event.key == pygame.K_p and turn == 'player':
                    ok, amt = player.use_item('potion')
                    if ok:
                        message = f"Used Potion: restored {amt} HP."
                        turn = 'enemy'
                    else:
                        message = "No potions left."

        # enemy turn
        if turn == 'enemy':
            alive_enemies = [e for e in enemies if e.is_alive()]
            if not alive_enemies:
                # wave cleared, give rewards and level up
                total_exp = 0
                total_gold = 0
                drops = {}
                for e in enemies:
                    total_exp += e.exp
                    total_gold += e.gold
                    d = e.drop_loot()
                    for k,v in d.items():
                        if k == 'gold':
                            total_gold += v
                        else:
                            player.items[k] = player.items.get(k,0) + v
                            drops[k] = drops.get(k,0) + v
                player.gold += total_gold
                lvlups, messages = player.gain_exp(total_exp)
                msg = f"Wave cleared! Gained {total_exp} EXP and {total_gold} G."
                if drops:
                    msg += " Drops: " + ", ".join([f"{k} x{v}" for k,v in drops.items()])
                message = msg
                # progress wave
                wave += 1
                player.mp = min(player.max_mp, player.mp + 12)
                enemies = make_wave(wave)
                selected_enemy = 0
                turn = 'player'
            else:
                actor = random.choice(alive_enemies)
                act_name, dmg, crit = actor.act(player, wave)
                message = f"{actor.name} used {act_name}: dealt {dmg} dmg{' (CRIT)' if crit else ''}"
                turn = 'player'
                if not player.is_alive():
                    message = "You were defeated... Returning to title."
                    save_game(player,1)
                    pygame.time.wait(1200)
                    # reset player as penalty
                    from player import Player as P
                    player = P()
                    wave = 1
                    enemies = make_wave(wave)
                    turn = 'player'

        # draw
        screen.fill((10,10,30))
        # background placeholder
        # enemies
        for idx, e in enumerate(enemies):
            ex = 80 + idx*260
            ey = 120
            color = (190,50,50) if e.is_alive() else (80,80,80)
            pygame.draw.rect(screen, color, (ex,ey,140,140))
            draw_text(screen, e.name, ex, ey-26, 22)
            draw_text(screen, f"HP: {e.hp}/{e.max_hp}", ex, ey+146, 18)
            if idx == selected_enemy:
                pygame.draw.rect(screen, (255,255,0), (ex-4,ey-4,148,148), 3)
        # player box
        pygame.draw.rect(screen, (40,40,120), (40,350,820,150))
        draw_text(screen, f"{player.name} Lv{player.level} - HP: {player.hp}/{player.max_hp}  MP: {player.mp}/{player.max_mp}", 60, 368, 22)
        draw_text(screen, f"EXP: {player.exp}/{player.next_exp}  Gold: {player.gold}", 60, 400, 18)
        draw_text(screen, f"Items: {player.items}", 60, 428, 18)
        # actions
        pygame.draw.rect(screen, (100,100,100), (40,520,160,64))
        draw_text(screen, "Attack (A)", 70, 538, 20)
        pygame.draw.rect(screen, (100,100,100), (230,520,160,64))
        draw_text(screen, "Fire (F)", 270, 538, 20)
        pygame.draw.rect(screen, (100,100,100), (420,520,160,64))
        draw_text(screen, "Ice (I)", 470, 538, 20)
        pygame.draw.rect(screen, (100,100,100), (610,520,160,64))
        draw_text(screen, "Heal (H)", 650, 538, 20)
        pygame.draw.rect(screen, (100,100,100), (800,520,80,64))
        draw_text(screen, "Potion(P)", 810, 538, 14)
        # message
        draw_text(screen, message, 40, 20, 26)
        draw_text(screen, f"Wave: {wave}", 780, 20, 20)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
