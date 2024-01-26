from card import Card
from random import randint
from time import sleep

class Team:
    """handles team to team communication."""
    def __init__(self,*args: Card):
        if len(args) > 5: raise IndexError('Team size is greater than four people.')
        self.group = [arg for arg in args] #distributes all inputs into group.

        self.graveyard = [] #all dead members go here.

        self.turn_amt = 0

    
    def choose_starg_enemy(self,other:object,ai=False) -> object:
        """prompts for a single enemy target."""
        if ai == False:
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
        
    def choose_alltarg_enemy(self,other:object,ai=False) -> list:
        """prompts for confirmation on all enemy targets."""
        if ai == False:
            option = "Target: All\n"
            user = input(option+"\ninput any to cancel, or 'Enter' to continue: ")
            if user != "":
                return None
        return other.group
        
        
    def choose_starg_ally(self,ai=False) -> object:
        """prompts for a single ally target."""
        if ai == False:
            option = "Target:\n"
            for i,x in enumerate(self.group):
                option += f"{i+1}. {x}\n"
            user = int(input(option+"\ninput: "))
            if user-1 <= len(self):
                return self.group[user]
            else:
                return None
        else:
            return self.group[randint(0,len(self)-1)]
        
    def choose_alltarg_ally(self,ai=False) -> list:
        """prompts for confirmation on all ally targets."""
        if ai == False:
            option = "Target: All\n"
            user = input(option+"\ninput any to cancel, or 'Enter' to continue: ")
            if user != "":
                return None
        return self.group

    def turn(self,other: list,ai=False):
        """allows the user to act during combat. if ai is True, the user will choose their moves automatically."""

        while self.turn_amt > 0 and (self.wipedout() == False or other.wipedout() == False):
            turn_passed = False
            #grabs first in line in group, and moves them to the back.
            member = self.group.pop(0)
            self.group.append(member)

            
            if member.isdead == False:
                while turn_passed == False:
                    member.cycle()
                    if member.stunned:
                        print(f'{member} cannot move!')
                        turn_passed = True
                        continue
                    print(f'Turns left: {self.turn_amt}')
                    user = ''
                    
                    if ai:
                        if member.len_skill() > 0:
                            user = str(randint(1,2))
                        else:
                            user = '1'
                        
                    else:
                        user = input(f"current: {member.get_info()}\n{member.move_menu()}\ninput: ")

                    #handles user input during combat menu.
                    if user.isdigit():
                        user = int(user)
                    else:
                        continue

                    if user == 1:
                        #assumed single-target
                        target = self.choose_starg_enemy(other,ai)
                        
                        if target != None:
                                print(member.attack(target))
                                if other.wipedout(): 
                                    return #exit turns because targets are all dead.
                                turn_passed = True
                        
                        

                    elif user == 2:
                        
                        if ai:
                            if member.silenced:
                                continue
                            
                            
                            user2 = randint(1,member.len_skill())
                            

                        else:
                            if member.silenced:
                                print('Cannot cast any skills!')
                                continue
                            user2 = int(input(member.cast_menu()+"\ninput: "))

                        #handles user input during skill menu.
                        if user2 == 0: #return to menu.
                            continue

                        if user2 <= member.len_skill() and user2 > 0: #skills.
                            skill_in_use = member.power[user2-1]
                            
                            if skill_in_use.target == 1:
                                target = self.choose_starg_enemy(other,ai)
                            elif skill_in_use.target >= 4:
                                target = self.choose_alltarg_enemy(other,ai)

                            
                            if target != None:
                                print(member.cast(skill_in_use,target))
                                if other.wipedout(): 
                                    return #exit turns because targets are all dead.
                                turn_passed = True

                    
                        else:
                            raise IndexError(f'Skill <{user2}> does not exist.')

                    elif user == 3:
                        member.passing()
                        turn_passed = True
            
            sleep(0.8)
            self.turn_amt = member.turn(self.turn_amt)
                      
                    
    def agi_shuffle(self):
            """agility shuffle:
            organizes the group by order of greatest agility. called at the start of player round."""
            agility = [member.c_modf[3] for member in self.group] 
            q = []
            for i in range(len(self.group)):
                for j in range(i,len(self.group)):
                    if agility[j]<agility[i]:
                        self.group[i],self.group[j]=self.group[j],self.group[i]
                        agility[i],agility[j]=agility[j],agility[i]
                agility.pop(0)
                
                q.insert(0,self.group[0])

                self.group.pop(0)

            self.group = q
    
    def _wiped(self):
        for idx in range(len(self.group)):
            if self.group[idx].isdead:
                self.graveyard.insert(0,self.group[idx])
                self.group[idx] = None
        while None in self.group:
            self.group.remove(None)
        
            

    def wipedout(self) -> bool:
        """checks if all party members are dead. if they are, they are banished into the graveyard."""
        self._wiped()
        if (len(self) == 0):
            return True
        return False


    def cycle(self):
        """completes all listed actions on round start."""
        self.agi_shuffle()
        self.turn_amt = len(self.group)
        print('')

    def lvl_up(self,xp: int):
        """applies xp gain to all members. levels up if possible."""
        for member in self.group:
            member.lvl_up(xp)

    def replenish(self):
        """restores hp and mp to max values."""
        for member in self.group:
            member.replenish()

    def __len__(self):
        return len(self.group)
    
