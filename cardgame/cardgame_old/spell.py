
import abc
from random import randint


class BaseTrait(abc.ABC):
    """handles the initialization and behaviors of all passive spells.
    
    current functions:
    * _passive - called on cycle.
    * cycle"""
    def __init__(self):
        pass

    @abc.abstractmethod
    def _passive(self):
        """Any sideeffects of the spell that is automatically casted on a turn start after certain conditions are met."""
        pass
    
    def cycle(self):
        self._passive()
        
class BaseSpell(abc.ABC):
    """handles the behavior structure of all active spells.
    
    current functions:
    * active"""
    def __init__(self, name: str, desc: str, type: int, level: int):
        self.name = name
        self.desc = desc
        self.type = type
        self.level = level
        
    @abc.abstractmethod
    def active(self,other) -> float:
        """main effect of the spell. must be deliberately used to take effect.
        
        returns in a list:
        - dmg [int]
        - spell info [str]
        - ailment [class]"""
        pass
        
class DamageSpell(BaseSpell):
    """handles the initialization and behaviors of active damaging spells."""

    def __init__(self,name: str, desc: str, type: int, level: int, dmg: int):
        self.dmg = dmg        
        super().__init__(name,desc,type,level)

    def _active(self, other: object):
        """handles calculation side. returns final damage value. assumes only single target."""
        typ_adv = other.spirit.type[self.type]
        if typ_adv > 1:
            pass
        return self.dmg * typ_adv
    
    def active(self,other: object) -> str:
        other.damaged(self._active(other))
        return f"uses {self.name}!"
        
class AOEDamageSpell(DamageSpell):

    def active(self,others: list):
        for other in others:
            super().active(other)
        return f"uses {self.name}!"



    def __str__(self):
        return f"{self.type} {self.level}|{self.name}: {self.desc}"

class StatSpell(BaseSpell):
    pass


class Ailment(abc.ABC):
    
    def __init__(self,chance, turn):
        
        self.chance = chance
        self.max_turn = turn
        self.turn = 0
        
    @abc.abstractclassmethod
    
    def _chance_effect(self):
        pass

    def _chance_apply(self):
        
        if randint(0,100)/100 == self.chance/100:
            self._chance_effect()
        
    def _passive(self):
        
        if self.turn > 0:
            self.active()
            self.length -= 1
        else:
            #must remove class
            pass
    
    @abc.abstractmethod
    def active(self):
        """defines what happens when this ailment is in effect."""
        
    def cycle(self):
        self._passive()


class BaseSpirit(abc.ABC):

    def __init__(self, trait=None, skill1=None, skill2=None, summon=None):
        """Used primarily to handle the abilities of a card.
        Acts as the base root of all Spirit class definitions.
        
        Initializes with no abilities."""

        self._abl = [trait,summon,skill1,skill2]
        #passive ability. usually set for each card.

        #special ability. Cannot be overwritten.

        #skill 1. set for each card.
        #skill 2. additional innate ability. is not always present.


        #instance variables.
        
    def _cast_smn(self):
        
        if self._abl[1] != None:
            return self._abl[1].active()
        return f"Spell not found."

    def _cast_one(self):
        
        if self._abl[2] != None:
            return self._abl[2].active()
    
    def _cast_two(self):

        if self._abl[3] != None:
            return self._abl[3].active()


    def used_option(self,cast_opt,other):
        """handles the casting of spells."""
        if cast_opt == 0 and self._abl[1]:
            self._cast_smn(other)
        elif cast_opt == 1 and self._abl[2]:
            self._cast_one(other)
        elif cast_opt == 2 and self._abl[3]:
            self._cast_two(other)
        else:
            print('No abilities found. Was it a mistake..?')

    def innate_options(self):
        """returns the skill options as a string."""
        final = f"0. {str(self._abl[1])}"
        if self._abl[2] != None: 
            final += f"\n1. {str(self._abl[2])}"
            if self._abl[3] != None: final += f"\n2. {str(self._abl[3])}"
            return final
        else: return final

    def cycle(self):
        """calls on beginning of player turn."""
        for spell in self._abl:
            if spell != None:
                spell.cycle()
        
    

    def __len__(self):
        return len(self._abl)


class Spirit(BaseSpirit):

    def __init__(self, name: str, desc: str, type: list, level: int, skills: list):
        self._name = name
        self._desc = desc

        self.type = type 
        """[protection, knowledge, confidence, charm, proficiency, kindness]
        
        utilizes multiplier table for calculating type weakness.
        generally, 1 means normal, 
        -1 is absorption to damage,
        0 is negation to damage, 
        0.5 is stronger defense against type, 
        2 is weaker against, and
        any higher is heavily weaker against.
        """
        self.lvl = level 
        """determines spell compatibility.
        
        *self >= spell compatibility means spell casted will be at its peak effectiveness.
        *self < spell compatibility means spell casted will have reduced effectiveness."""

        super().__init__(skills[0],skills[1],skills[2],skills[3])

    @property
    def name(self):
        return self._name

    def __str__(self):
        return f"{self.name}: {self._desc}"


