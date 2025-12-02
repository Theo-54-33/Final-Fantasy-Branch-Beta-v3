
import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess, sys, os
from shop import Shop
from save_manager import load, save

ROOT = os.path.dirname(__file__)
shop = Shop()

def start_game():
    python = sys.executable
    subprocess.Popen([python, os.path.join(ROOT, 'battle.py')])

def new_game():
    import player
    name = simpledialog.askstring("New Hero","Enter hero name:",initialvalue="Hero")
    if not name: return
    p = player.Player(name)
    save(p,1)
    messagebox.showinfo("New Game",f"Welcome {name}! Start the game now.")

def continue_game():
    p,wave = load()
    if not p:
        messagebox.showinfo("Continue","No saved game found.")
        return
    start_game()

def show_story():
    story = "A dark rift has appeared over the kingdom, releasing monsters. You are the heir to a legendary Guardian lineage. Defeat waves, recover fragments and face the final boss."
    messagebox.showinfo("Story",story)

def open_shop():
    p,_ = load()
    if not p:
        messagebox.showinfo("Shop","Start a game first.")
        return
    shop_win = tk.Toplevel(root)
    shop_win.title("Shop")
    tk.Label(shop_win,text=f"Gold: {p.gold}").pack()
    for key in shop.inventory.keys():
        item, qty = shop.inventory[key]
        tk.Button(shop_win,text=f"{item.name} - {item.price}G", command=lambda k=key: buy_item(k)).pack(pady=3)
    def buy_item(k):
        ok,msg = shop.buy(p,k)
        messagebox.showinfo("Shop",msg)
        save(p,1)
        shop_win.destroy()

root = tk.Tk()
root.title("FINAL FANTASY BRANCH BETA v3")
root.geometry('520x360')
tk.Label(root,text="FINAL FANTASY BRANCH BETA v3",font=('Helvetica',18,'bold')).pack(pady=10)
tk.Button(root,text="New Game",width=22,command=new_game).pack(pady=6)
tk.Button(root,text="Continue",width=22,command=continue_game).pack(pady=6)
tk.Button(root,text="Story",width=22,command=show_story).pack(pady=6)
tk.Button(root,text="Shop",width=22,command=open_shop).pack(pady=6)
tk.Button(root,text="Start Game",width=22,command=start_game).pack(pady=6)
tk.Button(root,text="Quit",width=22,command=root.quit).pack(pady=6)
root.mainloop()
