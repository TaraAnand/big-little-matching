import csv 
from collections import defaultdict
import sys
import math

class BLMatcher(object):
    """
    Each object contains a dictionary for littles and bigs. 
    The little dictionary connects each little with a set of their big preferences 
    The big dictionary connects each big with set of their little preferences 
    """
    def __init__(self, littlesPref, bigsPref):
        self.little_prefs = {}
        self.big_prefs = {}
        self.bigs_matched = {}
        self.pairs = []    

        self.collect_little_prefs(littlesPref)
        self.collect_big_prefs(bigsPref)
        self.fill_in_prefs()

        self.lrank = defaultdict(dict)
        self.brank = defaultdict(dict)

        for b, prefs in self.big_prefs.items(): 
            for i, l in enumerate(prefs): 
                self.brank[b][l] = i

        for l, prefs in self.little_prefs.items(): 
            for i, b in enumerate(prefs): 
                self.lrank[l][b] = i

        print("little_prefs")
        print(self.little_prefs)
        print("big_prefs")
        print(self.big_prefs)
        print("bigs_matched")
        print(self.bigs_matched)
        print("pairs")
        print(self.pairs)
        print("lrank")
        print(self.lrank)
        print("brank")
        print(self.brank)
     
        self.match()


    """
    Given the preference sheets for littles, establish preference list dictionaries
    """

    def collect_little_prefs(self, littlesPref):
        data = open(littlesPref, 'r')      
        responses = list(csv.reader(data))
        responses.pop(0)

        for little in responses:
        	self.little_prefs[little[1]] = [little[x] for x in range(3, 11)]

        return None

    """
    Given the preference sheets for bigs, establish preference list dictionaries
    """

    def collect_big_prefs(self, bigsPref):
        data = open(bigsPref, 'r')      
        responses = list(csv.reader(data))
        responses.pop(0)

        extra = len(self.little_prefs.keys()) - len(responses)

        for big in responses:
            self.big_prefs[big[1]] = [big[x] for x in range(3, 11)]
            if (extra > 0 and (big[13] == "twins plz" or big[13] == "huge lin huge lin huge lin")):
                twinbig = big[1] + "2"
                twinbigrep = [big[x] for x in range(2, len(big))] 
                twinbigrep.insert(0, twinbig)       #add name 
                twinbigrep.insert(0, big[0])        #copy timestamp 
                responses.append(twinbigrep)        #add copied line to end of list
                extra -= 1
            print(extra)
        return None 

    """
    Fill in preferences for the rest of the respective bigs/littles randomly 
    """
    def fill_in_prefs(self): 
        for little in self.little_prefs.keys(): 
            for big in self.big_prefs.keys():
                print("BIG")
                print(big) 
                if big not in self.little_prefs[little]: 
                    check = big[0:len(big)-1]
                    print("doble?")
                    print(check)
                    if check in self.little_prefs[little]: 
                        index = self.little_prefs[little].index(check)
                        self.little_prefs[little].insert(index+1, big)
                        print(little)
                        print(self.little_prefs[little])
                        continue
                    self.little_prefs[little].append(big)
                print(little)
                print(self.little_prefs[little])

        for big in self.big_prefs.keys(): 
            for little in self.little_prefs.keys(): 
                if little not in self.big_prefs[big]: 
                    self.big_prefs[big].append(little)


    """
    Test whether big prefers l over lit (current little match)
    """
    def prefers(self, b, l, lit): 
        return self.brank[b][l] < self.brank[b][lit]

    """
    If first choice is already matched, try the next choice.
    Returns the next choice big for a given little
    """
    def next_choice(self, l, b): 
        i = self.lrank[l][b] + 1
        if i >= len(self.little_prefs[l]): 
            return ""

        return self.little_prefs[l][i]

    """
    Match littles with their next preferred big
    """
    def match(self, littles=None, next=None, bigs=None):
        if littles is None: 
            littles = self.little_prefs.keys()
        if next is None: 
            next = {l:rank[0] for l, rank in self.little_prefs.items()}
        if bigs is None: 
            bigs = {}                       #mappings of bigs to current little matches
        if not len(littles): 
            self.pairs = [(lit, b) for b, lit in self.big_prefs.items()]
            self.bigs_matched = bigs 
            return bigs 
        l, littles = list(littles)[0], list(littles)[1:]
        b = next[l]
        if b != "":                         #next big to try to match little with 
            next[l] = self.next_choice(l, b) 

            if b in bigs:
                lit = bigs[b]                   #current little
                if self.prefers(b, l, lit):
                    littles.append(lit)
                    bigs[b] = l
                else: 
                    littles.append(l)
            else: 
                bigs[b] = l
        return self.match(littles, next, bigs)

    """
    """
    def create_pref_spreadsheet(self):
        filename = "preferences.csv"
        file = open(filename, 'w')
        filewriter = csv.writer(file, delimiter=',', quotechar='"')
        fieldnames = ['Big', 'Suggested Little', 'Big Rank', 'Little Rank', 'Rematch?']
        filewriter = csv.DictWriter(file, fieldnames=fieldnames)
        filewriter.writeheader()

        for match in self.bigs_matched.keys(): 
            big = match 
            little = self.bigs_matched[match]
            bigRank = self.brank[big][little]
            littleRank = self.lrank[little][big]
            rematch = False
            if littleRank > 5 or big == "": 
                rematch = True

            filewriter.writerow({'Big':big, 'Suggested Little':little, 'Big Rank':bigRank, 'Little Rank':littleRank, 'Rematch?':rematch})
        for little in self.little_prefs.keys(): 
            if little not in self.bigs_matched.values(): 
                big = ""
                bigRank = math.inf 
                littleRank = math.inf 
                if littleRank > 5 or big == "": 
                    rematch = True
                filewriter.writerow({'Big':big, 'Suggested Little':little, 'Big Rank':bigRank, 'Little Rank':littleRank, 'Rematch?':rematch})
        return None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Run program with command 'python biglittle.py [littlePrefSheet] [bigPrefSheet]'")
    else:
        matcher = BLMatcher(sys.argv[1], sys.argv[2])
        matcher.create_pref_spreadsheet()

        print("Matches")
        print(matcher.bigs_matched)
    
