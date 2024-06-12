"""
TO-DO:

P1
Be able to equip armor and heal outside of a fight.
replace do you want to look at inventory with an inv command

P2
Illnesses + Apothecarys

P3
Move Data into Class Object
 
FEATURES:
- Uses Prims Algorthim for generating map (https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- Fully Customizable (all editable through data table)
"""

import random, time, copy, sys
 
def Weapon(name, damage, desc, value, uses=-1):return {"type": "weapon", "name": name, "damage": damage, "uses": uses, "desc": desc, "value":value}
def Monster(name, weapons, desc, hp, damage, catchphrase, attackphrase): return {"type": "mob", "name": name, "weapons": weapons, "desc": desc, "hp": hp, "damage": damage, "catchphrase": catchphrase, "attackphrase": attackphrase}
def Loot(name, desc, value):return {"type": "loot", "name": name, "desc": desc, "value":value}
def Sale(name, desc, value, damage=-1, objecttype=None, uses=-1):
    if objecttype == "weapon": return {"type": "weapon", "name": name, "damage": damage, "uses": uses, "desc": desc, "purchased":[True, time.time()], "value":value}
    else: return {"type":"loot", "name":name, "desc":desc, "value":value, "purchased":[True, time.time()]}
def Armor(name, desc, av, value):return {"type":"protection", "name":name, "desc":desc, "av":av, "value":value}
def Consumable(name, desc, value, hv):return {"type":"consumable", "name":name, "desc":desc, "value":value, "hv":hv}
def Boss(name, weapons, desc, hp, damage, catchphrase, attackphrase): return {"type": "boss", "name": name, "weapons": weapons, "desc": desc, "hp": hp, "damage": damage, "catchphrase": catchphrase, "attackphrase": attackphrase}

def Action(t, monster):
    if t == "a":
        game.attack(monster)
        if monster["hp"] > 0: game.monsterattack(monster)
            
    if t == "b":
        if random.random() > 0.7:
            print("you have befriended {}! it walks away.".format(monster["name"]))
            monster["hp"] = 0
        else:
            print("you try to talk to {} but it dosent understand you. it attacks you!".format(monster["name"]))
            game.monsterattack(monster)
            
    if t == "w":
        game.wear()
            
    if t == "e":
        game.eat()
    
    if t == "s": 
        game.shop(data["player"])
        return

data = {
    "player": {
        "tokens": 10,
        "damage": 2,
        "health": 25,
        "inventory": [],
        "armor":None
    },
    "rooms": [
        {"name":"the dining room", "desc":"eat up! before the king turns you into stew"},
        {"name":"the ballroom", "desc":"where the partys are"},
        {"name":"the hall", "desc":"a huge area showing the kings immense wealth"},
        {"name":"the palace courtyard", "desc":"a beautiful garden nearby"},
        {"name":"the gates", "desc":"one of the many entrance to the palace"},
        {"name":"the weaponroom", "desc":"where the king keeps their guards weapons"},
        {"name":"the kitchen", "desc":"where the chefs cook up the kings food"},
        {"name":"the wine cellar", "desc":"did you know the easiest way to poision the king is through the wine?"},
        {"name":"the kings guestroom", "desc":"where the king puts his dukes when they visit him"}
    ],
    "bosses": [
        Boss("The King", [], "The one.", 25, 3, "ALL HAIL ME", "YOU DARE CHALLENGE ME?")
    ],
    "shopkeeper": [
        Sale("a fedora", "pretty!", 10),
        Sale("a fedora (but with a feather on top", "may no one know why the shopkeeper charges so much", 50)
    ],
    "monsters": [
        Monster("the gate guards", [], "only obeys the king", 5, 2, "you may not go through", "FOR THE KING!"),
        Monster("the slave", [], "a chained up fellow", 3, 1, "sorry but i have to attack you", "for the king!"),
        Monster("the tastetester", [], "makes sure the kings food is not posion", 2, 3, "welcome young one...", "i was going to try this but you can instead!"),
        Monster("the queen", [], "the king's wife", 10, 3, "oh my husband will be soo mad!", "ATTACK!")
    ],
    "loot": [
        Consumable("apple pie", "tastes like apple", 3, 3),
        Loot("templars coin", "the king has put a 2 pound bounty on this coin, just to find out more", 2)
    ],
    "options": [
        ["a", "attack"],
        ["w", "wear"],
        ["e", "eat"],
        ["s", "shop"]
        ]
}

data["player"]["maxhealth"] = data["player"]["health"]
for option in data["options"]: option.append(Action)
    
class Game:

    def __init__(self, data):
        self.data = data
        self.player = data["player"]
        self.rooms = data["rooms"]
        self.current_room = None

    def start(self):
        print("\n" * 300)
        print("""
 ____ ____ ____ ____ ____ ____
||r |||o |||y |||a |||l |||e ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|
a text-based adventure game by aram
loading...
              """)
        room = self.Room(100, 100)
        data["rooms"] = room.build_rooms()
        self.rooms = data["rooms"]
        self.enter(random.choice(self.rooms))
    
    def enter(self, room):
        self.current_room = room
        entermessages = ["you have entered {}", "you stumble upon {}", "you find yourself in {}", "you appear to be in {}", "you have appeared in {}", "you are in {}", "you are now in {}"]
        entermessage = random.choice(entermessages)
        print(entermessage.format(room["name"]))

        if not room["looted"]:
            if not room["monsters"]:  # check if predefined monsters in room
                if random.random() < 0.5:  # if not, 50% chance room is empty
                    print("this room is empty")
                else:
                    room["monsters"] = [random.choice(self.data["monsters"])]
                    print("there is something in this room...")
                    for monster in room["monsters"]:
                        print("{} - {}".format(monster["name"], monster["desc"]))
                    self.treasure(room)
            else:
                print("there is something in this room...")
                for monster in room["monsters"]:
                    print("{} - {}".format(monster["name"], monster["desc"]))
                self.treasure(room)
        else:
            print("this room is empty")

        self.search()

    
    def viewinv(self, inventory):
        for i in inventory: print(i["name"], "-", i["desc"])
                
    def fight(self, monster):
        print(monster["catchphrase"])
        while monster["hp"] > 0 and self.player["health"] > 0:
            print("choose an action:")
            for option in data["options"]:
                print("({}){}".format(option[0], option[1]))
                    
            action = input()
            
            for option in data["options"]:
                if option[0] == action: 
                    option[2](action, monster)
            
    def attack(self, monster):
        damage = self.player["damage"]
        monster["hp"] -= damage
        print("you hit {} for {} damage. it has {} hp left.".format(monster["name"], damage, monster["hp"]))
        
    def monsterattack(self, monster):
        damage = monster["damage"]
        if not self.player["armor"]:
            self.player["health"] -= damage
            print("\t" + monster["attackphrase"])
            print("it attacks you for {} damage. you have {} hp left.".format(damage, self.player["health"]))
        else:
            if self.player["armor"]["av"] > damage:
                self.player["armor"]["av"] -= damage
                print("\t" + monster["attackphrase"])
                print("it attacks you for {} damage. your armor saved you and now has {} av left.".format(damage, self.player["armor"]["av"]))
            else:
                damage -= self.player["armor"]["av"]
                self.player["armor"] = None
                self.player["health"] -= damage
                print("\t" + monster["attackphrase"])
                print("it attacks you for {} damage. yout shield protected some of the damage but broke. You have {} hp left.".format(damage, self.player["health"]))
    
    def choose(self, current):
        rooms = current["exits"]
        while True:
            print("===\ndirections\n===")
            for room in rooms:
                print(room)
            
            choice = input("choose an direction to go.").lower()
            
            if choice == "west": d = "east"
            elif choice == "east": d = "west"
            elif choice == "north": d = "south"
            elif choice == "south": d = "north"
            
            try: 
                c = rooms[choice]
                break
            except: 
                print("invalid direction! try again.")
        
        c["exits"][d] = self.current_room
        
        return c
                      
    def treasure(self, room):
        for monster in room["monsters"]:
            self.fight(monster)
        self.search()
        room["monsters"] = []
        self.search()

    def search(self):
        if self.current_room["looted"]:
            print("you already looted this room.")
        else:
            loot = random.choice(self.data["loot"])
            print("\nyou found {}!".format(loot["name"]))
            if input("would you like to read more about it? (y/n)") == "y":
                print("\n", loot["name"])
                print("\t", loot["desc"], "\n")
            self.player["inventory"].append(copy.deepcopy(loot))
            print("{} was added to your inventory".format(loot["name"]))
            self.current_room["looted"] = True

        next_room = self.choose(self.current_room)
        if next_room["type"] == "merchant":
            self.shop(self.player)
        else:
            self.enter(next_room)
        
    
    def shop(self, player):
        canceled = False
        def inventorysell(player):
            while True:
                for i, item in enumerate(player["inventory"]):
                    i += 1
                    print("({}) {} - {} tokens".format(i, item["name"], item["value"]))
                choice = input("enter item number (or c to cancel)")
                if choice != "c":
                    try: 
                        choice = self.player["inventory"][int(choice) - 1]
                        break
                    except: 
                        print("invalid choice! try again")
                else:
                    canceled = True
                return choice
        
        print("you currently have {} tokens.".format(self.player["tokens"]))
        if input("would you like to sell an item in your inventory?") == "y":
            if not player["inventory"]: print("you have nothing to sell!")
            else:
                sold = inventorysell(player)
                if not canceled:
                  self.player["tokens"] += sold["value"]
                  print("sold {} for {} tokens".format(sold["name"], sold["value"]))
                  player["inventory"].remove(sold)
        cart = []
        while True:
            while True:
                print("========")
                print("THE SHOP")
                print("========")
                print("the shopkeeper welcomes you. he says that everything is for sale (except his dog)")
                print("you currently have {} tokens".format(self.player["tokens"]))
                for i, item in enumerate(data["shopkeeper"]):
                    if item not in cart:
                        i += 1
                        print("({}) {} - {} tokens".format(i, item["name"], item["value"]))
                c = input("input a number (or c to cancel)")
                if c != "c":
                    try: 
                        c = data["shopkeeper"][int(c) - 1]
                        break
                    
                    except: print("invalid choice! you must input a number")
                else: 
                    if self.player["tokens"] >= c["value"]:
                        self.player["tokens"] -= c["value"]
                        self.player["inventory"].append(c)
                        data["shopkeeper"].remove(c)
                        print("\n" * 30)
                        print("bought {} for {} tokens".format(c["name"], c["value"]))
                        print("you now have {} tokens".format(self.player["tokens"]))
                        player = self.player
                    else: return

    def eat(self):
        foods = [item for item in data["player"]["inventory"] if item["type"] == "consumable"]
        
        if foods:
            while True:
                print("choose an item to eat:")
                for i, food in enumerate(foods):
                    print("({}) {} - {} health".format(i + 1, food["name"], food["hv"]))
        
                choice = input()
                
                try: 
                    choice = food[int(choice) + 1]
                    break
                except: print("invalid Option, try again.")
            
            if data["player"]["maxhealth"] == data["player"]["health"]:
                if data["player"]["health"] + choice["hv"] <= data["player"]["maxhealth"]: data["player"]["health"] += choice["hv"]
                else: data["player"]["health"] = data["player"]["maxhealth"]
                print("ate {} for {} health. you are now at {} health.".format(choice["name"], choice["hv"], data["player"]["health"]))
                data["player"]["inventory"].remove(choice)
                    
            else:
                print("you are at max health!")
        
        else:
            print("you don't have any food!")
    
    def wear(self):
        armors = [item for item in data["player"]["inventory"] if item["type"] == "protection"]
        
        if armors:
            print("choose an armor piece to wear:")
            
            while True:
                for i, armor in enumerate(armors):
                    print("({}) {} - {} av".format(i, armor["name"], armor["av"]))
                
                choice = input()
                
                try: 
                    choice = armors[int(choice)]
                    break
                
                except: print("invalid choice, try again.")
            
            if data["player"]["armor"]:
                data["player"]["inventory"].append(data["player"]["armor"])
                print("Unequipped {}".format(data["player"]["armor"]["name"]))
                data["player"]["armor"] = None
                
            data["player"]["armor"] = choice
            print("Equipped {} ᕙ(⇀‸↼‶)ᕗ".format(data["player"]["armor"]["name"]))
            
            data["player"]["inventory"].remove(choice)
            game.monsterattack(monster)
        else:
            print("you have nothing to equip!")
            
    def boss(self, boss):
        print("you have entered the boss room. prepare yourself for the final battle.")
        print("୧༼ಠ益ಠ༽୨")
        self.fight(boss)
        if boss["hp"] <= 0:
            print("you have defeated the boss! congratulations!")
        else:
            print("you have been defeated by the boss. game over.")
            print("""
 ____ ____ ____ ____ ____ ____ _________ ____ ____ ____
||t |||h |||a |||n |||k |||s |||       |||f |||o |||r ||
||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|
 ____ ____ ____ ____ ____ ____ ____
||p |||l |||a |||y |||i |||n |||g ||
||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|

a game by aram 
\( ﾟヮﾟ)/
                  """)
            sys.exit()
            
    class Room: # Prims Algorthim
        
        def __init__(self, height, width):
            self.height = height
            self.width = width
            
        def select_random_and_remove(self, cells):
            return cells.pop(random.randint(0,len(cells)-1))
        
        def is_unprocessed(self, cells, width, height, idxRow, idxColumn):
            return (idxRow >= 0 and idxColumn >= 0 and idxRow < height and idxColumn < width and len(cells[idxRow * width + idxColumn]["exits"]) == 0)
        
        def append_unprocessed(self, target, cells, width, height, idxRow, idxColumn):
            if self.is_unprocessed(cells, width, height, idxRow, idxColumn):
                target.append(cells[idxRow * width + idxColumn])
        
        def get_unprocessed_neighbors(self, cells, width, height, idxRow, idxColumn):
            n = []
            self.append_unprocessed(n, cells, width, height, idxRow-1, idxColumn)
            self.append_unprocessed(n, cells, width, height, idxRow, idxColumn-1)
            self.append_unprocessed(n, cells, width, height, idxRow+1, idxColumn)
            self.append_unprocessed(n, cells, width, height, idxRow, idxColumn+1)
            return n    
            
        def link_cells(self, c1, c2):
            if c1["x"] < c2["x"]:
                c1["exits"]["east"] = c2
                c2["exits"]["west"] = c1
            elif c1["x"] > c2["x"]:
                c1["exits"]["west"] = c2
                c2["exits"]["east"] = c1
            elif c1["y"] < c2["y"]:
                c1["exits"]["south"] = c2
                c2["exits"]["north"] = c1
            elif c1["y"] > c2["y"]:
                c1["exits"]["north"] = c2
                c2["exits"]["south"] = c1
            else:
                raise Exception("invalid cell linkage")
                
            
        def build_rooms(self):
            width, height = self.width, self.height
            
            # initialize cells
            cells = []
            for x in range(0,width):
                for y in range(0, height):
                    room = random.choice(data["rooms"])
                    monsters = []
                    try:
                        if room["monsters"]: monsters = room["monsters"]
                    except: monsters = []
                    cells.append({"type": "room", "name": room["name"], "desc": room["desc"], "monsters": monsters, "looted":False, "x":x, "y":y, "exits":{}})
            
            # initialize frontier    
            frontier = []
            this_cell = cells[random.randint(0, len(cells)-1)]
            frontier.append(this_cell)
                               
            while len(frontier) > 0:
                room = self.select_random_and_remove(frontier)
                neighbors = self.get_unprocessed_neighbors(cells, width, height, room["x"], room["y"])
                if(len(neighbors) > 0):   
                    neighbor = random.choice(neighbors)
                    self.link_cells(room, neighbor)
                    frontier.append(neighbor)
                    frontier.append(room)
                    
            return cells
        
game = Game(data)
game.start()