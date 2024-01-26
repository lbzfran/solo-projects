from random import randint

class Card:
    def __init__(self,soul: object):
        """this class handles all operations and communications with other cards.
        
        container for souls."""

        """for testing only:"""
        #self.power = [Tspell['1'],Tspell['6'],Tspell['7'],Tspell['8']]
        #self.stats = [50,50,10,5,12,10] #hp,mp,str,spd,magi,luck
        #self.type = [0.75,1.5,1,0.5,1]
        """end debug."""
        
        

        """implements soul."""
        self.soul = soul


        #modified statistics for combat purposes.        
        self.c_modf = [x for x in self.stats]
        self.c_type = [x for x in self.type]

        
        self.on_effects = []

        #state-bools
        self.silenced = False
        self.passed = False
        self.stunned = False
        self.critted = False
        self.rocked = False
        self.isdead = False
    
    def __str__(self):
        return self.soul.name

    @property
    def power(self):
        return self.soul.power
    
    @property
    def stats(self):
        return self.soul.stats
    
    @property
    def type(self):
        return self.soul.type

    @property
    def hp(self):
        return self.c_modf[0]
    
    @property
    def max_hp(self):
        return self.stats[0]

    def move_menu(self) -> str:
        """returns string of moves possible in combat menu."""
        return "1. Attack\n2. Skill\n3. Pass"
    
    def cast_menu(self) -> str:
        """returns string of moves possible in skill menu."""
        text = 'Skills\n0. Cancel\n'
        for i in range(len(self.power)):
            text += f"{i+1}. {self.power[i]}: {self.power[i].description}\n"
        return text

    def turn(self,cturn:int) -> int:
        """calculates and returns the number of turns used."""
        if self.rocked:
            self.rocked = False
            return cturn * 0
        elif self.critted or self.passed:
            self.critted = False
            return cturn - 0.5
            
        return cturn - 1
    
    def attack(self,other:object) -> str:
        dmg = self.stats[2] * other.type[0]
        print(f"{self} attacks!")
        return other.damaged(self.crit(dmg))
    
    def crit(self,dmg) -> int:
        if randint(1,100)/100 <= 0.2:
            self.critted = True
            print('Critical hit!')
            return dmg * 1.5
        return dmg

    def check_element(self,skill_type,other) -> str:

        text = ""
        if other.type[skill_type] > 1:
            text= 'Elemental weakness!'
            self.critted = True
        elif other.type[skill_type] == 0:
            text= 'Attack negated!'
            self.rocked = True
        return text

    def damaged(self,dmg:int) -> str:
        """calculates the damage taken, and returns a string representing such."""
        if self.isdead:
            return f'{self} is already knocked out!'
        else:
            self.c_modf[0] -= dmg
            text = f"{self} took {dmg} damage! "
            if self.c_modf[0] <= 0:
                self.c_modf[0] = 0
                self.isdead = True
                text += f"{self} has been knocked out!"
            return text
    
    def afflicted(self,buff: object) -> str:
        """inflicts a buff onto self, and returns string representing such."""
        if buff not in self.on_effects:
            self.on_effects.append(buff)
            return f"{self} has been inflicted with {buff}!"
        else:
            return f"Infliction already exists!"


    def passing(self):
        if self.passed != True:
            self.passed = True
            
    def cast(self,skill: object,other) -> str:
        """passes self and other onto skill object."""
        print(f"{self} uses {str(skill)}!")
        return skill.cast(self,other)

    
    
    def get_info(self):
        return f"{self}: {int(self.hp)}/{self.max_hp}"
    
    def cycle(self):
        if len(self.on_effects) > 0:
            for effect in self.on_effects:
                if effect.cycle(self) == False:
                    print(f"{effect} has worn off!")
                    self.on_effects.remove(effect)
        if self.passed:
            self.passed = False
    
    def lvl_up(self,xp: int):
        print(f"{self} has gained {xp} experience!")
        self.soul.gain_xp(xp)

    def replenish(self):
        for i in range(2):
            self.c_modf[i] = self.stats[i]

    def __le__(self,other):
        if self.stats[3] >= other.stats[3]:
            return True
        else:
            return False
    
    def len_skill(self)-> int:
        return len(self.power)
