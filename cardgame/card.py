
"""
Cards are used to attack and cast spells.


"""
from random import randint
from math import sqrt

class Card:
    def __init__(self,card_type: int,name: str,description: str,action_type: bool,cost: int,val: float,typ: int,chn = 0,effect = 0,target = 1,repeat = 1):
        self._ctp = card_type

        self._name = name
        self._desc = description

        # controls whether card uses stamina or mana.
        self._atp = action_type
        self._cost = cost

        self._val = val
        self._type = typ

        self._chn = chn
        self._efc = effect

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
    def atype(self):
        return self._atp

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
                # stamina check
                amt = caster.sp - cin.cost
                if amt < 0:
                    print("Not enough stamina!")
                    return 4
                caster.sp = amt
            case 1:
                # mana check
                amt = caster.mp - cin.cost
                if amt < 0:
                    print("Not enough mana!")
                    return 4
                caster.mp = amt
            case 2:
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
                # skip commented lines
                fullDeck[str(idx)] = Card(int(attr[0]),str(attr[1]),str(attr[2]),bool(attr[3]),int(attr[4]),float(attr[5]),int(attr[6]),float(attr[7]),int(attr[8]),int(attr[9]),int(attr[10]))
                idx += 1
    return fullDeck


if __name__ == "__main__":
    deck = import_full_deck()
    print("Deck:")
    for key in deck.keys():
        text = ''
        text += f"{key} {deck[key]}: {deck[key].desc} //"
        if deck[key].ctype == 1 or deck[key].ctype == 3:
            text += f" dmg: {deck[key].val}"
        if deck[key].ctype == 2 or deck[key].ctype == 3:
            text += f" chance: {deck[key].chance*100}%"
        print(text)
