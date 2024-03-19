
"""
Cards are used to attack and cast spells.


"""
from random import randint
from math import sqrt

class Card:
    def __init__(self,card_type: int,name: str,description: str,cost: int,val = 0.0,typ = 1,chance = 0,effect = 0,target = 1,repeat = 1):
        self._ctp = card_type # DMG, BUFF, ABF

        self._name = name
        self._desc = description

        # controls whether card uses health or mana.
        self._cost = cost

        # Damage var
        self._val = val
        self._type = typ

        # Buff var
        self._chn = chance
        self._efc = effect

        # General var
        self._trg = target
        self._rpt = repeat

    def __str__(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def ctype(self):
        return self._ctp

    @property
    def cost(self):
        return self._cost

    @property
    def val(self):
        return self._val

    @property
    def typ(self):
        return self._type

    @property
    def chance(self):
        return self._chn

    @property
    def effect(self):
        return self._efc

    @property
    def target(self):
        return self._trg

    @property
    def repeat(self):
        return self._rpt


class Control:
    def __init__(self,cards: list):

        #contains list of useable cards.
        self._deck = cards

    def _attack(self,caster,other,card) -> str:
        #attacks must always have 'caster','other' and a 'card' to reference.

        bDmg = card.val

        # DAMAGE CALCULATIONS (only user stats)
        if card.atype == 1:
            #take intel if mana-based
            uStat = caster.statTable[4]
            cDmg = (caster.lvl + uStat) * bDmg / 15
        else:
            #take strength if not mana
            uStat = caster.statTable[3]
            cDmg = uStat * bDmg / 15

        idx = 0
        if isinstance(other,list):
            dmg = []
            for enemy in other:

                # enemy type advantage
                oType = enemy.typeTable[card.typ]

                # takes calculated damage and reduces by each enemy's resists
                fDmg = cDmg / sqrt((enemy.statTable[1]*8)+enemy.dfs) * oType #* (3841 + randint(0,256)/4096)

                dmg.append([fDmg for _ in range(card.repeat)])
                idx += 1

        elif isinstance(other,object):

            oType = other.typeTable[card.typ] # 0, 0.5, 1, 1.5

            fDmg = cDmg / sqrt((other.statTable[1]*8)+enemy.dfs) * oType

            dmg = [fDmg for _ in range(card.repeat)]
            idx += 1
        else:
            raise ValueError("'other' datatype is invalid: ", type(other))

        # processes ui output
        text = ''
        while idx > 0:
            # dmg calculation and representation
            idx -= 1

        return text

    def _chancecalc(self,chance:int,repeat:int) -> bool:
        for _ in range(repeat):
            if randint(0,100) / 100 <= chance:
                return True
        return False

    def _skill(self,caster,other,card,rout: bool) -> str:

        text = ''
        chance = (luck * 0.25) / 100 + card.chance

        if isinstance(other,list):
            apply = [self._chancecalc(chance,card.repeat) for x in len(other)-1]

            for idx, applied in enumerate(apply):
                if applied:
                    # apply it
                    pass
                else:
                    text += f"{other[idx]} could not be afflicted!\n"

        elif isinstance(other,object):
            apply = self._chancecalc(chance,card.repeat)
            if apply:
                # apply it
                pass
            else:
                text += f"{other} could not be afflicted!\n"
        else:
            return ValueError("'other' datatype is invalid: ", type(other))

        return text


    def _replacedeck(self,newcards: list):
        self._deck = list(newcards)

    def cast(self,caster,other,cnum: int) -> int:

        # int return cases:
        # 0: cast success.
        # 1: base error. something failed.
        # 2: input error.
        # 4: cost not met.

        if cnum > len(self._deck)-1:
            #input index must exist in deck.
            print("Card not found.")
            return 2

        cin = self._deck[cnum]

        text = ''

        # checks if cost can be met
        match cin.atype:
            case 0:
                # mana check
                amt = caster.mp - cin.cost
                if amt < 0:
                    print("Not enough mana!")
                    return 4
                caster.mp = amt
            case 1:
                # health check
                amt = caster.hp - cin.cost
                if amt <= 0:
                    print("Not enough health!")
                    return 4
                caster.hp = amt
            case _:
                raise ValueError("'atype' of selected card invalid: ", cin.atype)


        attacked = False

        # 1: ATK, 2: SPL, 3: ATK & SPL
        if cin.ctype == 1 or cin.ctype == 3:
            attacked = True
            text += self._attack(caster,other,cin)

        if cin.ctype == 2 or cin.ctype == 3:
            text += self._skill(caster,other,cin,attacked)




def import_full_deck():
    fullDeck = {}
    with open("deck.txt","r") as deck:
        rdeck = deck.read().splitlines()
        idx = 0
        for line in rdeck:
            attr = line.split(",")
            if attr[0].isdigit():
                # skips commented lines in .txt file
                #                   Card(CARDTYPE,NAME,DESC,ATYPE,
                                #   COST,VAL,TYPE,CHANCE,EFFECT REF,
                                #   TARGET,REPEAT)

                if int(attr[0]) == 1:
                    fullDeck[str(idx)] = Card(card_type=int(attr[0]),
                                              name=str(attr[1]),
                                              description=str(attr[2]),
                                              cost=int(attr[3]),
                                              val=int(attr[4]),
                                              typ=int(attr[5]),
                                              target=int(attr[6]),
                                              repeat=int(attr[7]))

                if int(attr[0]) == 2:
                    fullDeck[str(idx)] = Card(card_type=int(attr[0]),
                                              name=str(attr[1]),
                                              description=str(attr[2]),
                                              cost=int(attr[3]),
                                              chance=float(attr[4]),
                                              effect=int(attr[5]),
                                              target=int(attr[6]),
                                              repeat=int(attr[7]))
                if int(attr[0]) == 3:
                    fullDeck[str(idx)] = Card(card_type=int(attr[0]),
                                              name=str(attr[1]),
                                              description=str(attr[2]),
                                              cost=int(attr[3]),
                                              val=int(attr[4]),
                                              typ=int(attr[5]),
                                              chance=float(attr[6]),
                                              effect=int(attr[7]),
                                              target=int(attr[8]),
                                              repeat=int(attr[9]))
                idx += 1
    return fullDeck

"""
    _CARD TYPES_
     Damage
     Buff
     DMG & BUFF
     Modifier: can be chained with other card types to modify their effects.
     EX of Mods:
    Reversal: if applicable, swaps the card type to its 'reversed' form.
"""

if __name__ == "__main__":
    deck = import_full_deck()
    print("Deck:")
    for key in deck.keys():
        text = ''
        text += f"{key} {deck[key]}: {deck[key].desc} // cost: {deck[key].cost}"
        if deck[key].ctype == 1 or deck[key].ctype == 3:
            text += f" dmg: {deck[key].val}"
        if deck[key].ctype == 2 or deck[key].ctype == 3:
            text += f" chance: {deck[key].chance*100}%"
        print(text)
