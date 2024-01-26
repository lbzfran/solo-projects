
from card import Card
from team import Team
from random import randint
from soul import Tsoul


if __name__ == '__main__':
    team1 = Team(Card(Tsoul['x01']),Card(Tsoul['x03']))
    team2 = Team(Card(Tsoul['x02']),Card(Tsoul['x04']))

    for team in [team1,team2]: #for debugging only
        team.lvl_up(randint(50,500))
        team.replenish()

    while team1.wipedout() == False or team2.wipedout() == False:

        print('\n//TEAM 1 TURN//')
        team1.cycle()
        team1.turn(team2)
        
        if team2.wipedout():
            break

        print('\n//TEAM 2 TURN//')
        team2.cycle()
        team2.turn(team1,ai = True)
        
        if team1.wipedout():
            break


#TODO: 
#current known bug: Souls are somehow sharing the exact same stats when levelling up..?
#fixed. assignment, mutation, reference.
#https://www.pythonmorsels.com/pointers/