
from abc import ABC,abstractmethod
from random import randint

class Effect(ABC):
    """Changes the state of a unit to some extent."""
    def __init__(self,name,description,duration,strength,type):
        self._name = name
        self._desc = description
        self._dur = duration
        self._dmg = strength
        self._type = type

    @abstractmethod
    def _effect(self,unit):
        pass 

    def cycle(self,unit)-> bool:
        """Checks duration. if effect in place, will return True, else False, which prompts removal of effect instance."""
        if self._dur >= 0:
            self._effect(unit)
            self._dur -= randint(1,2)
            return True
        return False

    def add_dur(self,amt: int):
        """adds value to the current length of duration."""
        self._dur += amt

    def __str__(self) -> str:
        return self._name
    
    @property
    def duration(self) -> int:
        return self._dur

    @property
    def description(self) -> str:
        return self._desc
    
    @property
    def strength(self) -> int:
        return self._dmg
    
    @property
    def type(self) -> int:
        return self._type

class StunEffect(Effect):
    """Effect that disables the ability to act during a turn.
    UNIVERSAL: does not have a unique descriptor"""
    def __init__(self,name,description,duration,strength,type):
        super().__init__(name,description,duration,strength,type)
        self.inited = False

    def _effect(self,unit):
        if self.inited == False:
            unit.stunned = True
            self.inited = True
        elif self.duration <= 0:
            unit.stunned = False
            return False
        return True


    def cycle(self,unit):
        """initializes the stat changes on cast by calling this function."""
        if self.inited:
            return super().cycle(unit) #calls with duration decrease.
        else:
            self._effect(unit) #calls without decreasing duration.
            return True

class DotEffect(Effect):
    """Effect that damages a unit during their turn.
    will inflict damage on start of every turn.
    CONTEXTUAL: descriptor is determined case-by-case."""
    def __init__(self,name,description,duration,strength: int,type: int):
        super().__init__(name,description,duration,strength,type)
    
    def _effect(self,unit)-> str:
        text = f"{unit} is {self.description}.\n"
        if self.duration > 0:
            text += f'{unit.damaged(self._dmg * unit.type[self._type])}'
        return text

class StatEffect(Effect):
    """Effect that improves/weakens a unit for a duration.
    UNIVERSAL: does not have a unique descriptor."""
    def __init__(self,name,description,duration,strength: int,type: int):
        super().__init__(name,description,duration,strength,type)
        self.inited = False

    def _effect(self,unit)-> str:
        #FIXME: does not properly initialize on cast.
        if self.inited == False:
            unit.c_modf[self._type] += self._dmg
            self.inited = True
            
        elif self._dur <= 0: #revert changes
            unit.c_modf[self._type] -= self._dmg
            return False
        return True

    def cycle(self,unit):
        """initializes the stat changes on cast by calling this function."""
        if self.inited:
            return super().cycle(unit) #calls with duration decrease.
        else:
            self._effect(unit) #calls without decreasing duration.
            return True
        
class SilenceEffect(Effect):
    """Effect that disables a unit's ability to use skills for a duration."""
    def __init__(self,name,description,duration,strength,type):
        super().__init__(name,description,duration,strength,type)

    def _effect(self,unit):
        if self.duration > 0:
            unit.silenced = True
        else:
            unit.silenced = False

class TypeEffect(Effect):
    """Effect that changes the resistance value of a unit for a duration.
    UNIVERSAL: does not have a unique descriptor."""
    def __init__(self,name,description,duration,strength,type):
        super().__init__(name,description,duration,strength,type)
        self._inited = False

    def _effect(self,unit):
        if self.inited == False:
            unit.c_type[self._type] += self._dmg
            self.inited = True
        elif self._dur <= 0: #revert changes
            unit.c_type[self._type] -= self._dmg
            return False
        return True

    def cycle(self,unit):
        """initializes the stat changes on cast by calling this function."""
        if self.inited:
            return super().cycle(unit) #calls with duration decrease.
        else:
            self._effect(unit) #calls without decreasing duration.
            return True
