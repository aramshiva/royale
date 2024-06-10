"""
TO-DO:

P1
If a room has a monster AND a treasure, you get the option to grab the treasure and the monster doesn't attack.  If you go away and return to the room, the monster is no longer there. (you get the "already looted" message)
Be able to equip armor and heal outside of a fight.
replace do you want to look at inventory with an inv command

P2
Boss Fights
Illnesses + Apothecarys
Bet (roll a dice during a boss which has 3 HORRIBLE options and 3 GREAT options and one of the terrible options will kill you next damage)
Data Saving + Save Slots

P3
Clean Up Text
Move Data into Class Object
 
FEATURES:
- Uses Prims Algorthim for generating map (https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- Fully Customizable (all editable through data table)
"""
import random, time, copy
 
def Weapon(name, damage, desc, value, uses=-1): 
    return {"type": "weapon", "name": name, "damage": damage, "uses": uses, "desc": desc, "value":value}

def Monster(name, weapons, desc, hp, damage, catchphrase, attackphrase): 
    return {"type": "mob", "name": name, "weapons": weapons, "desc": desc, "hp": hp, "damage": damage, "catchphrase": catchphrase, "attackphrase": attackphrase}

def Boss(name, desc, hp, damage, catchphrase):
    return {"type":"boss", "name":name, "desc":desc, "hp":hp, "damage":damage, "catchphrase":catchphrase}

def Loot(name, desc, value): 
    return {"type": "loot", "name": name, "desc": desc, "value":value}
 
def Sale(name, desc, value, damage=-1, objecttype=None, uses=-1):
    if objecttype == "weapon": return {"type": "weapon", "name": name, "damage": damage, "uses": uses, "desc": desc, "purchased":[True, time.time()], "value":value}
    else: return {"type":"loot", "name":name, "desc":desc, "value":value, "purchased":[True, time.time()]}

def Armor(name, desc, av, value):
    return {"type":"protection", "name":name, "desc":desc, "av":av, "value":value}

def Consumable(name, desc, value, hv):
    return {"type":"consumable", "name":name, "desc":desc, "value":value, "hv":hv}

def Action(t, monster):
    if t == "a":
        game.attack(monster)
        if monster["hp"] > 0:
            game.monsterattack(monster)
            
    # if t == "r":
    #     if random.random() < 0.5:
    #         print("You ran away!")
    #         return
    #     else:
    #         print("You tried to run away but you tripped!")
    #         game.monsterattack(monster)
            
    if t == "b":
        if random.random() > 0.7:
            print("You have befriended {}! It walks away.".format(monster["name"]))
            monster["hp"] = 0
        else:
            print("You try to talk to {} but it dosent understand you. It attacks you!".format(monster["name"]))
            game.monsterattack(monster)
            
    if t == "w":
        armors = [item for item in data["player"]["inventory"] if item["type"] == "protection"]
        
        if armors:
            print("Choose an armor piece to wear:")
            
            while True:
                for i, armor in enumerate(armors):
                    print("({}) {} - {} av".format(i, armor["name"], armor["av"]))
                
                choice = input()
                
                try: 
                    choice = armors[int(choice)]
                    break
                
                except: print("Invalid Option, try again.")
            
            if data["player"]["armor"]:
                data["player"]["inventory"].append(data["player"]["armor"])
                print("Unequipped {}".format(data["player"]["armor"]["name"]))
                data["player"]["armor"] = None
                
            data["player"]["armor"] = choice
            print("Equipped {}".format(data["player"]["armor"]["name"]))
            
            data["player"]["inventory"].remove(choice)
            game.monsterattack(monster)
        else:
            print("You have nothing to equip!")
            
    if t == "e":
        foods = [item for item in data["player"]["inventory"] if item["type"] == "consumable"]
        
        if foods:
            while True:
                print("Choose an item to eat:")
                for i, food in enumerate(foods):
                    print("({}) {} - {} health".format(i + 1, food["name"], food["hv"]))
        
                choice = input()
                
                try: 
                    choice = food[int(choice) + 1]
                    break
                except: print("Invalid Option, try again.")
            
            if data["player"]["maxhealth"] == data["player"]["health"]:
                if data["player"]["health"] + choice["hv"] <= data["player"]["maxhealth"]: data["player"]["health"] += choice["hv"]
                else: data["player"]["health"] = data["player"]["maxhealth"]
                print("Ate {} for {} health. You are now at {} health.".format(choice["name"], choice["hv"], data["player"]["health"]))
                data["player"]["inventory"].remove(choice)
                    
            else:
                print("You are at max health!")
        
        else:
            print("You don't have any food!")
    
    if t == "s": 
        game.shop(data["player"])
        return

data = {
    "player": {
        "tokens": 10,
        "damage": 10,
        "health": 100,
        "maxhealth": 100,
        "inventory": [
            Weapon("Wooden Stick", 1, "The stick is transcribed with some sort of unfamiliar language.", 1)
        ],
        "armor":None
    },
    "rooms": [
        {"name":"The Classroom", "desc":"Learn or else..."},
        {"name":"The Stage", "desc":"Showtime!"},
        {"name":"Library", "desc":"Silence in the library!"},
        {"name":"Mysterious room", "desc":"..."}
    ],
    "shopkeeper": [
        Sale("1 use blade", "Powerful but you only have a single hit, use wisely!", 5, 12, "weapon", 1),
        Sale("Fedora", "Look Stylish!", 3)
    ],
    "monsters": [
        Monster("The Director", [], "A sinister figure overseeing everything.", 20, 5, "The show is starting!", "You cannot escape!"),
        Monster("The Toymaker", [], "A creepy toymaker with a malevolent grin.", 15, 4, "Welcome to my workshop!", "Let's play a game!"),
        Monster("The Doctor", [], "A doctor with a questionable practice.", 18, 3, "Time for your check-up!", "This won't hurt a bit!"),
        Monster("The Librarian", [], "A ghostly figure who guards forbidden knowledge.", 12, 3, "Silence in the library!", "Knowledge is power!"),
        Monster("The Butcher", [], "A hulking figure wielding a bloody cleaver.", 25, 6, "Fresh meat!", "I'll carve you up!")
    ],
    "loot": [
        Consumable("Apple Pie", "Yum!", 5, 10),
        Loot("Creepy Doll", "A doll with eyes that seem to follow you.", 1),
        Loot("Mystery Potion", "A potion with swirling contents.", 3),
        Loot("Old Key", "An old key with intricate designs.", 4),
        Loot("Ancient Tome", "A book filled with strange symbols.", 5),
        Loot("Rusty Cleaver", "An old, rusty cleaver with dried blood.", 6),
        Loot("Mechanical Heart", "A heart made of gears and metal.", 7),
        Armor("Chainmail Armor", "Weak but useful!", 3, 3),
        Armor("Templar's Armor", "Embroidered with gold!", 9, 15)
    ],
    "options": [
        ["a", "attack"],
        # ["r", "run"],
        ["b", "befriend"],
        ["w", "wear"],
        ["e", "eat"],
        ["s", "shop"]
        ]
}

for option in data["options"]: option.append(Action)
    
class Game:

    def __init__(self, data):
        self.data = data
        self.player = data["player"]
        self.rooms = data["rooms"]
        self.current_room = None
    
    class Room:
        
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

    def start(self):
        print("\n" * 300)
        print("""
 ____ ____ ____ ____ ____ ____
||r |||o |||y |||a |||l |||e ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|
A game by aram
a text-based adventure game
loading...
              """)
        room = self.Room(30, 30)
        data["rooms"] = room.build_rooms()
        self.rooms = data["rooms"]
        self.enter(random.choice(self.rooms))
    
    def enter(self, room):
        self.current_room = room
        entermessages = ["You have entered {}","You stumble upon {}","You find your self in {}","You appear to be in {}","You have appeared in {}","You are in {}","You are now in {}"]
        entermessage = random.choice(entermessages)
        print(entermessage.format(room["name"]))

        if not room["monsters"]: # check if predefined monsters in room
            if random.random() < 0.5: # if not, 50% chance room is empty
                if not room["looted"]:
                    room["monsters"] = [random.choice(self.data["monsters"])]
                    print("There is something in this room...")
                    for monster in room["monsters"]:
                        print("{} - {}".format(monster["name"], monster["desc"]))
                        self.fight(monster)
            else:
                print("This room is empty")

        else:
            if not room["looted"]:
                print("There is something in this room...")
                for monster in room["monsters"]:
                    print("{} - {}".format(monster["name"], monster["desc"]))
                    self.fight(monster)
                
        self.search()
    
    def viewinv(self, inventory):
        for i in inventory: print(i["name"], "-", i["desc"])
                
    def fight(self, monster):
        print(monster["catchphrase"])
        while monster["hp"] > 0 and self.player["health"] > 0:
            print("Choose an action:")
            for option in data["options"]:
                print("({}){}".format(option[0], option[1]))
                    
            action = input()
            
            for option in data["options"]:
                if option[0] == action: 
                    option[2](action, monster)
            
    def attack(self, monster):
        damage = self.player["damage"]
        monster["hp"] -= damage
        print("You hit {} for {} damage. It has {} HP left.".format(monster["name"], damage, monster["hp"]))
        
    def monsterattack(self, monster):
        damage = monster["damage"]
        if not self.player["armor"]:
            self.player["health"] -= damage
            print("\t" + monster["attackphrase"])
            print("It attacks you for {} damage. You have {} HP left.".format(damage, self.player["health"]))
        else:
            if self.player["armor"]["av"] > damage:
                self.player["armor"]["av"] -= damage
                print("\t" + monster["attackphrase"])
                print("It attacks you for {} damage. Your armor saved you and now has {} AV left.".format(damage, self.player["armor"]["av"]))
            else:
                damage -= self.player["armor"]["av"]
                self.player["armor"] = None
                self.player["health"] -= damage
                print("\t" + monster["attackphrase"])
                print("It attacks you for {} damage. Your shield protected some of the damage but broke. You have {} HP left.".format(damage, self.player["health"]))
    
    def choose(self, current):
        rooms = current["exits"]
        while True:
            print("DIRECTIONS")
            for room in rooms:
                print(room.capitalize())
            
            choice = input("Choose an direction to go.").lower()
            
            if choice == "west": d = "east"
            elif choice == "east": d = "west"
            elif choice == "north": d = "south"
            elif choice == "south": d = "north"
            
            try: 
                c = rooms[choice]
                break
            except: 
                print("Invalid Direction! Try Again.")
        
        c["exits"][d] = self.current_room
        
        return c
                      
    def search(self):
        if self.current_room["looted"]:
            print("You already looted this room.")
        else:
            loot = random.choice(self.data["loot"])
            print("\nYou found {}!".format(loot["name"]))
            if input("Would you like to read more about it? (y/n)") == "y":
                print("\n", loot["name"])
                print("\t", loot["desc"], "\n")
            self.player["inventory"].append(copy.deepcopy(loot))
            if input("{} was added to your inventory.\n\tWould you like to see your inventory? (y/n)".format(loot["name"])) == "y":
                self.viewinv(self.player["inventory"])
            self.current_room["looted"] = True
    
        next_room = self.choose(self.current_room)
        if next_room["type"] == "merchant": self.shop(self.player)
        else: self.enter(next_room)
        
    
    def shop(self, player):
        canceled = False
        def inventorysell(player):
            while True:
                for i, item in enumerate(player["inventory"]):
                    i += 1
                    print("({}) {} - {} tokens".format(i, item["name"], item["value"]))
                choice = input("Enter item number (or c to cancel)")
                if choice != "c":
                    try: 
                        choice = self.player["inventory"][int(choice) - 1]
                        break
                    except: 
                        print("Invalid Choice! Try again")
                else:
                    canceled = True
                return choice
        
        print("You currently have {} tokens.".format(self.player["tokens"]))
        if input("Would you like to sell an item in your inventory?") == "y":
            if not player["inventory"]: print("You have nothing to sell!")
            else:
                sold = inventorysell(player)
                if not canceled:
                    self.player["tokens"] += sold["value"]
                    print("Sold {} for {} tokens".format(sold["name"], sold["value"]))
                    player["inventory"].remove(sold)
        cart = []
        while True:
            while True:
                print("========")
                print("THE SHOP")
                print("========")
                print("The shopkeeper welcomes you. He says that everything is for sale (except his dog)")
                print("You currently have {} tokens".format(self.player["tokens"]))
                for i, item in enumerate(data["shopkeeper"]):
                    if item not in cart:
                        i += 1
                        print("({}) {} - {} tokens".format(i, item["name"], item["value"]))
                c = input("Input a number (or c to cancel)")
                if c != "c":
                    try: 
                        c = data["shopkeeper"][int(c) - 1]
                        break
                    
                    except: print("Invalid Choice! You must input a number")
                else: 
                    if self.player["tokens"] >= c["value"]:
                        self.player["tokens"] -= c["value"]
                        self.player["inventory"].append(c)
                        data["shopkeeper"].remove(c)
                        print("\n" * 30)
                        print("Bought {} for {} tokens".format(c["name"], c["value"]))
                        print("You now have {} tokens".format(self.player["tokens"]))
                        player = self.player
                    else: return

game = Game(data)
game.start()