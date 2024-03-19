

def random_event():
    """Chooses a random event to start."""
    pass

def combatEvent(player: list, *enemies: list):
    """
    player: list of summons.
    enemies: list of lists of summons.
    """
    idx = 1
    totalRounds = len(enemies)
    for enemy in enemies:
        print(f"Round {idx} of {totalRounds}")
        while not player.isWiped() or not enemy.isWiped():
            player.info()
            player.cycle()
            player.playTurn(enemy)

            if enemy.isWiped():
                print("Enemy defeated!")
                break

            enemy.info()
            enemy.cycle()
            enemy.playTurn(player,True)

            if player.isWiped():
                print("Player defeated!")
                break
        idx += 1


if __name__ == "__main__":
    pass
