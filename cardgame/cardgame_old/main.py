
import card, stats, spell

def main():
    print('Combat test.')
    

    hero = card.Card(spell.Spirit("Fighter","Basic combatant.",[1,1,1,1,1,1],1,[None,None,None,None]),stats.Stat([20,20,3,2,2,2,2],1,1))
    enemy = card.Card(spell.Spirit("Reverse Fighter","Basic enemy combatant.",[1,1,1,1,1,1],1,[None,None,None,None]),stats.Stat([20,20,2,2,2,2,2],1,1))

    i=0
    while True:
        print(f"Turn {i}")
        hero.cycle()
        print(hero)
        print(hero.menu(enemy))
        if enemy.isDead:
            break
        enemy.cycle()
        print(enemy)
        print(enemy.menu(hero))
        if hero.isDead:
            break
        i+=1


main()