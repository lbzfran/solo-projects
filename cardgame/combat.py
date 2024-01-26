
from card import *
from summon import *




if __name__ == "__main__":
    # chapter reader
    Deck = import_full_deck()


    user = Team(Summon("Player","Find it here.",[1 for x in range(6)],[5 for y in range(5)],[Deck[str(x)] for x in range(2)],1000))
    enemy = Team(Summon("Common","Enemy of mankind.",[1 for x in range(6)],[2 for y in range(5)],[Deck[str(x)] for x in range(1)],1000))

    while not user.isWiped() or enemy.isWiped():
        user.info()
        user.cycle()
        user.playTurn(enemy)

        if enemy.isWiped():
            print("Enemy defeated!")
            break

        enemy.info()
        enemy.cycle()
        enemy.playTurn(user,True)

        if user.isWiped():
            print("Player defeated!")
            break