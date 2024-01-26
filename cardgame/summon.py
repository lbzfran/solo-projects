from card import Control
from random import randint
from time import sleep
class Summon:
    def __init__(self,name:str,description:str,typeTable: list, stats: list, deck: list,xp=0):
        self._name = name
        self._desc = description

        # handles all card use.
        self.control = Control(deck)

        # <body> improves hp.
        # <mind> fights stresses of magic. increases stress threshold.
        # <strength> improves physical attacks. [phys_atk = strength * 2.25]
        # <intelligence> improves magical attacks. [magi_atk = intel * 1.75]
        # <luck> affects chances in various aspects of the game.

        self.xp = 0
        self.lvl = 1
        self.statTable = list(stats)
        self.typeTable = list(typeTable)

        # combat-related values #
        self._maxhp = 1
        self._hp = self._maxhp

        self._maxStress = 20
        self._stress = 0

        self._rp = [0 for x in range(5)]

        # bool bar: [stunned]
        self._statusBar = [0 for x in range(3)]
        # object bar
        self._buffBar = []

        self._passed = False

        #initialization
        self.gainXp(xp,True)
        self.replenish()


    def __str__(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @property
    def maxhp(self):
        return self._maxhp

    @property
    def stress(self):
        return self._stress

    @property
    def maxStress(self):
        return self._maxStress

    @property
    def rp(self):
        return self._rp

    def findrp(self,idx):
        return self._rp[idx]

    @property
    def passed(self) -> bool:
        if self._passed:
            return True
        return False

    def togglePass(self):
        self._passed = True

    """stat control: BEGIN"""
    def damage(self,dmg):
        self._hp = round(self._hp - dmg,1)
        if self._hp < 0:
            self._hp = 0
        return f"{self} took {dmg} damage!"



    def _incStat(self,show: bool):

        text = ''
        stat_name = ['body','mind','str','int','luck']

        stat = randint(0,4)
        old = self.statTable[stat]
        self.statTable[stat] += randint(1,2)
        
        text += f"\n{stat_name[stat]}: {old} -> {self.statTable[stat]}"

        if show:
            return text
        return ""

    def _processCombat(self):
        self._maxhp = self.statTable[0] * 1.5 + self.statTable[2] * 0.5
        self._maxStress = 20 + self.statTable[1] * 2 + self.statTable[3] * 0.5

    def gainXp(self,xp: int,show=False):
        self.xp += xp
        print(f"{self} has gained {xp} experience!" + self.levelUp(show))

    def levelUp(self,show):
        
        text = ''
        start_lvl = self.lvl
        while self.lvl < 100 and self.xp >= (4 * pow(self.lvl,3) / 5):
            self.lvl += 1
            text += self._incStat(show)

        self._processCombat()
        
        levelCap = 1000 #FIXME

        text += f"\nLevel: {start_lvl} -> {self.lvl}\n" + f"current xp: {self.xp}\n"
        if self.lvl != levelCap:
            text += 'xp till next level: ' + str(4 * pow(self.lvl,3) / 5) + '\n'
        else:
            text += 'Max Level reached.\n'

        if show:
            return text
        return ""

    def replenish(self):
        self._hp = self.maxhp
        self._stress = 0
    """stat control: END"""
    """combat control: START"""
    def goTurn(self):
        pass

    def cycle(self):
        if len(self._buffBar) > 0:
            for effect in self._buffBar:
                if effect.cycle(self) == False:
                    print(f"{effect} has worn off!")
                    self._buffBar.remove(effect)
        if self.passed:
            self._passed = False

    def info(self):
        visual = f"  O  \n" + f" -+- \n" + f"  ^  \n"
        text = f"{self} // hp: {self.hp}/{self.maxhp} | stress: {self.stress}/{self.maxStress}\nRunes: {self.findrp(0)} {self.findrp(1)} {self.findrp(2)} {self.findrp(3)} {self.findrp(4)}\n"
        return visual + text

    def moveMenu(self):
        """returns string of moves possible in combat menu."""
        return "1. Deck\n2. Bag\n3. Pass"

class Team:
    def __init__(self,*args: Summon):
        if len(args) > 5: raise IndexError("Team Size greater than four.")
        self.group = [arg for arg in args]

        self.graveyard = []

        self.turnCount = 0

    def choose_strg_enemy(self,other,auto=False) -> object:
        """choose a single enemy in a group."""
        if not auto:
            option = "Target:\n"
            for i,x in enumerate(other.group):
                option += f"{i+1}. {x}\n"
            user = input(option+"\ninput: ")
            if user.isdigit() and (int(user)-1 <= len(other)):
                return other.group[int(user)-1]
            else:
                return None
        else:
            return other.group[randint(0,len(other)-1)]

    def choose_atrg_enemy(self,other,auto=False) -> list:
        """confirm targetting for all enemies in group."""
        if not auto:
            option = "Target: All\n"
            user = input(option+"\n'Enter' to continue, or input any and 'Enter' to cancel: ")
            if user != "":
                return None
        return other.group

    def choose_strg_ally(self):
        pass

    def choose_atrg_ally(self):
        pass

    def playTurn(self,other:list,auto=False):
        
        while self.turnCount > 0 and (not self.isWiped() or not other.isWiped()):
            turn_passed = False
            member = self.group.pop(0)
            self.group.append(member)

            if member.hp > 0:
                while turn_passed == False:
                    member.cycle()
                    if member._statusBar[0]: # check stun
                        print(f"{member} cannot move!")
                        turn_passed = True
                        continue
                    print(f"Turns left: {self.turnCount}")
                    user = ''

                    if auto:
                        user1 = "1"
                    else:
                        user1 = input(f"current: \n{member.info()}\n{member.moveMenu()}\ninput: ")

                    if user1.isdigit():
                        user1 = int(user1)
                    else:
                        continue

                    match user1:
                        case 1:
                            if auto:
                                user2 = randint(1,len(member.control))
                                # FIXME: improve ai over time to account for unusable skills
                            else:
                                user2 = int(input(member.control.cardMenu()+"\ninput: "))

                            if user2 == 0:
                                # returns to menu.
                                continue

                            if user2 <= len(member.control) and user2 > 0:
                                targCount = member.control.deck[user2-1].target

                                match targCount:
                                    case 0:
                                        target = self.choose_strg_ally()
                                    case 1:
                                        target = self.choose_strg_enemy(other,auto)
                                    case 4:
                                        target = self.choose_atrg_enemy(other,auto)
                                    case _:
                                        raise ValueError("card target invalid: ",targCount)

                                if target != None:
                                    check = member.control.cast(member,target,user2-1)
                                    match check:
                                        case 1:
                                            raise ValueError("Something broke during casting")
                                        case 2:
                                            print("Wrong input.")
                                            continue
                                        case 4:
                                            print("Cost wasn't met.")
                                            continue
                                    if other.isWiped():
                                        return
                                    turn_passed = True
                            else:
                                raise IndexError(f"Skill <{user2}> does not exist.")

                        case 2:
                            pass

                        case 3:
                            member.togglePass()
                            turn_passed = True

                        case _:
                            continue

            sleep(0.8)
            self.turnCount = self._calcTurn(self.turnCount,member.passed)        

    def _calcTurn(self,turn: int,didPass:bool):
        """calculates and returns the number of turns used."""
        if didPass:
            return turn - 0.5
        return turn - 1

    def _wiped(self):
        for idx in range(len(self)):
            if self.group[idx].hp <= 0:
                self.graveyard.insert(0,self.group[idx])
                self.group[idx] = None
        while None in self.group:
            self.group.remove(None)

    def isWiped(self) -> bool:
        self._wiped()
        if (len(self) == 0):
            return True
        return False

    def replenish(self):
        """restores hp to max value, and resets stress meter."""
        for member in self.group:
            member.replenish()

    def lvlUp(self,xp: int):
        for member in self.group:
            member.gainXp(xp)
    
    def cycle(self):
        self.turnCount = len(self)
        print()

    def info(self):
        for member in self.group:
            print(member.info())

    def __len__(self):
        return len(self.group)
    


"""
Attack:
Attacks are affected by element types.
Attacking someone with weaker affinity deals more damage.
likewise, damage could be mitigated, or even nullified by
targets with higher affinity.
Attacking against weaker affinities also grants the player
an extra turn (0.5)
Phys costs HP.
Magic costs runes.
Magic damage calculated using intel.
most magic can be "reversed", changing its effect.
This can be done by "gearshifting", or "rune-printing".
gearshifting can be used during battle, but costs extra (1.3x, rounded up) runes to use.
rune-printing is a semi-permanent reversal, but can only be done outside of battle.
Physical attacks cannot be affected by reversing.

Gearshifting has three different modes.
Reversal
Enchance


Three tiers of magic.
tier I  : 2-10 rune (component spells; most are upgraded to tier II versions)
R flames: increases physical damage.
N firebolt: light fire damage.
R bubble: creates a light shield around target.
N scattershot: light water damage. targets 2 random enemies.
R painleaf: heals target.
N rocktoss: light earth damage. chance to strike twice.
R AMP UP: increases magical damage.
N powerzap: light electric damage. chance to stun.
R darkstab: light dark damage.
N sharplight: light holy damage.
tier II : 11-30 rune (highest quantity of all tiers)
tier III: 30-40 rune (highest quality magic, very endgame)


"""