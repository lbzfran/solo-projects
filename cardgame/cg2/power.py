
from abc import ABC,abstractmethod
from random import randint
from effect import *


class Power(ABC):
    def __init__(self,name:str,description:str,target:int,repeat:int):
        self._name = name
        self._desc = description
        self._trg = target
        self._rpt = repeat

    @abstractmethod
    def cast(self):
        pass

    def __str__(self):
        return self._name
    
    @property
    def description(self) -> str:
        return self._desc

    @property
    def target(self) -> int:
        return self._trg
    
    @property
    def repeat(self) -> int:
        return self._rpt
    
    @property
    def base(self) -> int:
        """flexible definition. 
        
        refers to base damage in 'Attack' based powers.
        
        refers to infliction chance in 'Buff' based powers."""
        return self._base
    
    @property
    def type(self) -> int:
        """flexible definition. 
        
        refers to element type in 'Attack' based powers.
        
        refers to buff type in 'Buff' based powers."""
        return self._type

class AttackPower(Power):
    def __init__(self,name:str,description:str,base_dmg:int,elem_type:int,target = 1,repeat = 1):
        super().__init__(name,description,target,repeat)
        self._base = base_dmg
        self._type = elem_type

    def _attack(self, stat_magi: int, other: object) -> int:
        return (self.base + stat_magi) * other.type[self.type]

    def cast(self, unit: object, other: list) -> str:
        """passes the stat associated with 'magi', and the target 'other'."""
        
        stat_magi = unit.c_modf[4]
        if isinstance(other,list):
            dmg = []
            for enemy in other:
                perdmg = [self._attack(stat_magi,enemy) for _ in range(self.repeat)]
                dmg.append(perdmg) #if multiple targets, dmg becomes a list of lists of repeated damages.
        else:
            dmg = [self._attack(stat_magi,other) for _ in range(self.repeat)] #if single target, dmg is only one list of repeated damages.


        idx = 0
        text = ''
        while idx < self.repeat:
            if isinstance(other,list):
                for jidx,enemy in enumerate(other):
                    text += enemy.damaged(dmg[jidx][idx]) + '\n' + unit.check_element(self.type,enemy) + '\n'
            elif isinstance(other,object):
                text += other.damaged(dmg[idx]) + '\n' + unit.check_element(self.type,other) + '\n'
            else: # other's type is None.
                raise ValueError("'other' datatype is invalid: ",type(other))
            idx += 1
        return text
       
class BuffPower(Power):
    """power that inflicts 'effects' to some capacity."""
    def __init__(self,name,description,chance: float,buff_effect: Effect,target = 1,repeat = 1):
        super().__init__(name,description,target,repeat)
        self._base = chance
        self._type = buff_effect
        
    def _effect(self,chance)->bool:
        """Checks if effect will apply, given chance and number of repetitions."""
        for _ in range(self.repeat):
            if randint(0,100) / 100 <= chance:
                return True
        return False

    def cast(self,unit: object,other: list) -> str:
        """attempts to apply an effect onto target 'other'."""
        text = ''
        chance = (unit.c_modf[5] * 0.25) / 100 + self._base
        if isinstance(other,list):
            effective = []
            for _ in other:
                pereffect = self._effect(chance)
                effective.append(pereffect)
            
            for idx,truth in enumerate(effective):
                if truth:
                    text += other[idx].afflicted(self._type) + '\n'
                else:
                    text += f"{other[idx]} could not be afflicted!\n"
        else:
            effective = self._effect(chance)
            if effective:
                text += other.afflicted(self._type) + '\n'
            else:
                text += f"{other} could not be afflicted!\n"
        
        return text


#imports buffs and powers from text file.

def import_type():
    Tbuff = {}
    with open("buff.txt","r") as buff:

        rbuff = buff.read().splitlines()
        #read example:
        #format: PT,NM,DC,DR,STR,TYP
        # 1,Medo Stun,Distracted with a Bear.,2,0,0
        idx = 0
        for line in rbuff:
            attr = line.split(",")
            if attr[0] == "1":
                Tbuff[str(idx)] = StunEffect(str(attr[1]),str(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]))
                idx += 1
            elif attr[0] == "2":
                Tbuff[str(idx)] = DotEffect(str(attr[1]),str(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]))
                idx += 1
            elif attr[0] == "3":
                Tbuff[str(idx)] = StatEffect(str(attr[1]),str(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]))
                idx += 1
            elif attr[0] == "4":
                Tbuff[str(idx)] = SilenceEffect(str(attr[1]),str(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]))
                idx += 1
            elif attr[0] == "5":
                Tbuff[str(idx)] = TypeEffect(str(attr[1]),str(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]))
                idx += 1
    return Tbuff

def import_spell(Tbuff : dict):
    with open("power.txt","r") as power:
        rpower = power.read().splitlines()
        # read example:
        # basic power
        #format[1]: PT,NM,DC,DMG,TYP,TG,RP : format[2]: PT,NM,DC,CH,EF
        Tspell = {}
        idx = 0
        for line in rpower:
            attr = line.split(",")
            if attr[0] == "1":
                #attack power
                Tspell[str(idx)] = AttackPower(str(attr[1]),str(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]),int(attr[6]))
                idx += 1
            elif attr[0] == "2":
                #buff power (must reference predefined buff already.)
                Tspell[str(idx)] = BuffPower(str(attr[1]),str(attr[2]),float(attr[3]),Tbuff[attr[4]],int(attr[5]),int(attr[6]))
                idx += 1
    return Tspell


Tspell = import_spell(import_type())

if __name__ == "__main__":
    print("--All available powers--")
    for key in Tspell:
        print(key, '->', Tspell[key],Tspell[key].description)
    print("--end--")

"""
spelltable = {

    '1': AttackPower("Vatra",  "Light Fire Damage. Targets One Foe.",10,1), 
    '2': AttackPower("Vota",   "Light Water Damage. Targets One Foe.",10,2),
    '3': AttackPower("Dah",    "Light Wind Damage. Targets One Foe.",10,3),
    '4': AttackPower("Hrast",  "Light Earth Damage. Targets One Foe.",10,4),
    '5': AttackPower("Slava",  "Light Light Damage. Targets One Foe.",10,5),
    '6': AttackPower("Vecer",  "Light Dark Damage. Targets One Foe.",10,6),

    '7': AttackPower("Zasuti",   "Light Fire Damage. Targets All Foes. Chance to inflict smolder.",10,1,target=4),
    '8': AttackPower("Vodopad",  "Light Water Damage. Targets All Foes.",10,2,target=4),
    '9': AttackPower("Oluja",    "Light Wind Damage. Targets All Foes.",10,3,target=4),
    '10': AttackPower("Potres",  "Light Earth Damage. Targets All Foes. Chance to stun.",10,4,target=4),
    '11': AttackPower("Razapeti","Light Holy Damage. Targets All Foes. Chance to inflict blindness.",10,5,target=4),
    '12': AttackPower("Zakopati","Light Dark Damage. Targets All Foes. Chance to inflict weakness.",10,6,target=4),

    '13': AttackPower("Armi",    "Light Physical Damage. Targets one Foe. Repeats twice.",10,0,1,repeat=2),
    
    #'14': BuffPower("Heated",    "Increases 'ATK' stat. Targets One Ally."),
    #'15': BuffPower("Hydrated",  "Increases 'DEF' stat. Targets One Ally."),
    #'16': BuffPower("Nimble",    "Increases 'AGI' stat. Targets One Ally."),
    #'17': BuffPower("Naturally", "Increases 'LCK' stat. Targets One Ally."),
    #'18': BuffPower("Burnt Out", "Decreases 'ATK' stat. Targets One Enemy."),
    #'19': BuffPower("Wet",       "Decreases 'DEF' stat. Targets One Enemy."),
    #'20': BuffPower("Encumbered","Decreases 'AGI' stat. Targets One Enemy."),
    #'21': BuffPower("Tough Luck","Decreases 'LCK' stat. Targets One Enemy."),

    #light-grade special skills
    #'22': AttackPower("Poison", "Light Earth Damage. Chance to inflict poison."),
    #'23': AttackPower("")
    



    '16': AttackPower("Struja", "Chance to stun. Targets One Foe.",10,3),

    

    '17': BuffPower('Medo','Light chance to stun for two turns. Targets One Foe.',0.33,StunEffect('Medo Stun','distracted with a bear.')),
    '18': BuffPower('Rez','Medium chance to inflict bleed for two turns. Targets One Foe.',0.67,DotEffect('Bleed','losing blood.',duration=2,damage=10,type=0))
    }

"""


"""

#element types: [0:normal,1:fire,2:water,3:wind,4:earth,5:holy,6:dark]
#effect type: [0:bleed,1:smolder,2:frozen,3:unstable,4:poison,5:braced,6:fear]

bleed: take physical damage every turn. damage increases with duration.
(base_dmg + (base_vit * 1/5 * duration))
smolder: takes additional magic damage from all spells. reduces duration per spell hit. 
(10%_of_last_spell_dmg)
frozen: stuns target. attacks break the stun. physical attacks received will deal increased damage.

unstable: user's spell damage multiplier is increased, but attacking also damages the user. this damage can crit.
(2 * (attack_dmg + duration_passed))
poison: grass damage over time.
()
braced: all damage received is reduced, but attacks no longer miss.
()
fear: random chance for any action that uses a turn to fail.


#base effects:
bleed (dot): (bleed_dmg + (bleed_dmg * duration) / 3)
sleep (break-stun): (no form)
stun (stun): (no form)
weakness (stat): decreases a given stat.
brave (stat): increases a given stat.

#element effects:
smolder (fire,dot): dealt based on last damage taken. (burn_dmg + ( 2 * last_damage_taken / 5 ))
poison (earth,dot): weaker, but lasts longer. (poison_dmg + (poison_dmg * duration) / 6 )
frozen (water, break-stun): phys/earth break deals increased damage. (break_dmg + bonus_dmg)
petrify (earth, stun): water deals increased damage, and has a chance of insta-killing.
fear (dark, action): actions have a high chance of failing. (condition: randint(0,100) <= 0.2)

Inferno:
    canto
        i. shifting woods
        ii. descent beneath the mountains
        iii. the gate of hell, and the rivers of acheron: Charon
First Circle, Limbo: most neutral area of inferno. intellectuals are trapped here.
        iv. great castle
Second Circle, Lust: Minos, and Canto of the queens.
        v. unrelenting storm between ruined slopes



"""