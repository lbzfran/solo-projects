
from spell import Spirit, Ailment
from stats import Stat
from random import randint
class Card:
    """combines the classes will and stat. this class handles all operations and communications
    with other cards."""
    
    def __init__(self,spirit: Spirit,stat: Stat):
        
        self.spirit = spirit #handles card behavior.
        self.stat = stat #handles statistic behavior.
        
        #INSTANCE VARIABLES - FOR COMBAT
        self.c_stats = self.stat.refresh() 
        """ modifiable ver of base stats. 
        hp and mp reflects current values, 
        and other stats are additively combined on base stats."""
        
        self.turn = 0 
        """one given per turn start. 
        any option during combat will cost one of this.
        it is possible to gain more than one thru other means."""
        
        self.c_ailment: Ailment = None
        """defines the ailment the card is suffering from.
        will automatically use its effect on the card's turn."""
        
        self.isBlocking = False

        self.isDead = False
        
    def _turn_menu(self):
        
        return f"{self.spirit.name}'s Turn:\n1. Attack\n2. Innate Abilities\n3. Spellbook\n4. Block\n"
    
    def _innate_options(self):
        
        return self.spirit.innate_options()
    
    def menu(self,other):
        """currently, other is assumed to be a singular class. in the future, it will be treated as a list of classes."""

        user = input(self._turn_menu())
        if user == '1':
            action = self.attack(other)
        elif user == '2':
            action = self.spirit.used_option(int(input(self._innate_options())),other)
        elif user == '3':
            pass
        elif user == '4':
            action = self.block()
            
        return f"{self.spirit.name} {action}"

    def _attack(self,other):
        """basic strike. calculated using attack stat."""
        dmg = self.stat.b_stats[2] + self.c_stats[2]

        typ_adv = other.spirit.type[self.spirit.type[0]]

        mult = 1
        if randint(1,100)/100 <= 0.2:
            mult += 1

        return (dmg * typ_adv) * mult

    def attack(self,other):
        dmg = other.damaged(self._attack(other))

        return f'strikes {other.spirit.name} for {dmg}!'

    def _blocked(self,dmg = 0):
        """used to calculate the blocked damage."""
        if dmg != 0 and self.isBlocking:
            #takes the dmg argument and returns the unblocked damage.
            #currently only cuts damage in half.
            return dmg // 3
            

    def block(self):
        """blocks all incoming attacks for the rest of the turn. will use up all remaining turns of the card instantly."""
        self.isBlocking = True
        self.turn = 0
        return f"blocks!"
            
    def stats(self,full = False):
        """Returns the statistics of the card."""
        val = ""
        for idx,nm in enumerate(['HP','MP']):
            
            x = f"{nm}: {self.c_stats[idx]} / {self.stat.b_stats[idx]}\n"
            val += x
        
        if full:
            for idx,nm in enumerate(['ATK','MAG','DEF','SPD','LCK']):
                
                x = f"{nm}: {self.stat.b_stats[idx+2]+self.c_stats[idx+2]}\n"
                val += x
                
        return val
    
    def damaged(self,dmg: int):
        """passes dmg (times type advantage) to health.."""
        if self.isBlocking:
            dmg = self._blocked(dmg)

        self.c_stats[0] -= dmg
    
        if self.c_stats[0] <= 0: #sets hp to 0 if dead.
            self.c_stats[0] = 0
            self.isDead = True
        
        return dmg
    
    def _targets_menu(self,others: list):
        targets = ''
        for i, other in enumerate(others):
            print(f'{i+1}. {str(other)}')
    
    def target(self,others):
        input(self._targets_menu(others))


    def cycle(self):
        """automatically called on start of card's turn. 
        not called again on multiple continuous turns."""
        
        if self.isBlocking:
            print('Blocking ended.')
            self.isBlocking = False
        
        if self.c_ailment != None:
            self.c_ailment.cycle()

        self.spirit.cycle()
        
        
    def refresh(self):
        """non-combat ability. restores combat stats to its base equivalent."""
        self.c_stats = self.stat.refresh()
        self.c_ailment = None    
        

    def __str__(self):
        
        return str(self.spirit) + '\n' + self.stats()