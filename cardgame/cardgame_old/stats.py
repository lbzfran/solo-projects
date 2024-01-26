

class Stat:

    def __init__(self, stats: list, level: int, exp: int):
        
        self.b_stats = stats # base stats (only affected by levels): [hp,mp,attack,magic,defense,speed,luck]
        self.level = level #current level, 0 - 3
        self.exp = exp
        
        #controls the instance variables

        
    def refresh(self):
        
        return [self.b_stats[0],self.b_stats[1],0,0,0,0,0]





