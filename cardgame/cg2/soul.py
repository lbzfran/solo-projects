from power import Tspell
from random import randint
class Soul:
    """base form and levelling up."""    
    def __init__(self,name: str,description: str,type: list,lvltable: dict, base_stats = [50,50,10,5,12,10],xp=0):
        self.name = name
        self.desc = description
        
        self.power = []
        self.stats = list(base_stats)
        self.type = list(type)
        

        self.xp = xp
        self.lvl = 1
        self.lvltable = lvltable

        self.show_text = True

    def levelup(self) -> str:
        """handles levelling up of a soul."""
        text = ''
        start_lvl = self.lvl
        while self.lvl < 100 and self.xp >= (4 * pow(self.lvl,3) / 5):
            self.lvl += 1
            print(self._stat_inc())
        
        text += f"Level: {start_lvl} -> {self.lvl}\n" + self._check_avail_spells() + f'current xp: {self.xp}\n'
        if self.lvl != 100:
            text += 'xp till next level: ' + str(4 * pow(self.lvl,3) / 5) + '\n'
        else:
            text += 'Max Level reached.\n'
        
        if self.show_text:
            return text
        
        return ""

    
    def _check_avail_spells(self):
        "checks for every spell below or equal to current level requirements. learns all values that are true."
        text = ''
        for spell_lvl in self.lvltable:
            spell = self.lvltable[spell_lvl]
            if spell_lvl <= self.lvl and spell not in self.power:
                self.power.append(spell)
                text += f"New spell available: {spell}\n"
        return text
    
    def _stat_inc(self):
        "called on a level up. increases a random stat."
        
        text = ''
        stat_name = ['hp','mp','str','spd','magi','luck']

        #OPT 1: increases only one parameter, by a noticeable margin.
        stat = randint(0,5)
        if stat in [0,1]:
            old = self.stats[stat]
            self.stats[stat] += 6
        else:
            old = self.stats[stat]
            self.stats[stat] += randint(2,4)
        text += f"{stat_name[stat]}: {old} -> {self.stats[stat]}"

        if self.show_text:
            return text
        return ""
    
    def gain_xp(self,xp: int):
        self.xp += xp
        print(self.levelup())

    def toggle_text(self):
        #toggles show_text.
        if self.show_text == False:
            self.show_text = True
        else:
            self.show_text = False


#contains the levels in which a soul can attain certain spells. should not need to be imported in main.

def import_level(Tspell : dict):
    Tlevel = {}
    with open("level.txt","r") as level:
        rlevel = level.read().splitlines()
        #read example:
        #format: #format: [LV:PW],[LV:PW]...
        # 2:1,6:6
        idx = 0
        for line in rlevel:
            attrx = line.split(",")

            if "#" in attrx[0]:
                continue

            TTspell = {}
            skip_CS = False
            for scripture in attrx:
                if skip_CS == False:
                    skip_CS = True
                    continue
                attry = scripture.split(":")
                TTspell[int(attry[0])] = Tspell[str(attry[1])]
            
            Tlevel[attrx[0]] = TTspell
            idx += 1
    return Tlevel

def import_soul(Tlevel : dict):
    Tsoul = {}
    with open("soul.txt","r") as soul:
        rsoul = soul.read().splitlines()
        #read example:
        #format: PH,FI,WT,WD,ER,LT,DK
        # 1,0,0.5,1.5.2,1,1
        idx = 0
        for line in rsoul:
            attr = line.split(",")
            
            if "#" in attr[0]:
                continue
            
            Tsoul[str(attr[0])] = Soul(attr[1],attr[2],[float(attr[x]) for x in range(3,10)],Tlevel[attr[0]])
            idx += 1
    return Tsoul

Tsoul = import_soul(import_level(Tspell))

if __name__ == "__main__":
    print("--All available souls--")
    for key in Tsoul:
        print(key, '->', Tsoul[key].name,Tsoul[key].type)
    print("--end--")


"""
Ttype = {

}

#format: [LV:PW,...]
Tlevel = {
    "blaze"  : {2 : Tspell['1'], 6 : Tspell['6']},
    "wendigo": {2 : Tspell['2'], 6 : Tspell['5']},
    "cyborg" : {2 : Tspell['3'], 6 : Tspell['7']},
    "parasite":{2 : Tspell['4'], 6 : Tspell['8']}
}

#contains the foundation of a soul with 0 xp.

#format: NM,DC,TY,LV
Tsoul = {
    "blaze"   : Soul('Devil','Fire demon.', type = [1,0.5,1.5,1,1,1,1], lvltable = Tlevel['blaze']),
    "wendigo" : Soul('Wendigo','Ice beast.',type = [0.75,1.5,0.5,0,0,0,0], lvltable = Tlevel['wendigo']),
    "cyborg"  : Soul('Cyborg','Half Robot.',type = [0.75,1,1,0.5,1.5,1,1], lvltable = Tlevel['cyborg']),
    "parasite": Soul('Parasite','Invasive monster.', type = [1.5,1.5,1.5,1.5,1.5,1.5,1.5], lvltable = Tlevel['parasite'])
}

"""

if __name__ == "__main__":
    """edits soul table. can add, remove, etc."""
    
    pass
    
    
    
    