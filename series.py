import random

class WatchTimeHolder():
    def __init__(self):
        l = []
        for i in range(9):
            if i == 2: # computers count from 0 you dingus
                l.append([False]*13)
            else:
                l.append([False]*26)
        self.series = l
    
    def craftMessage(self):
        mes = ""
        for i, flags in enumerate(self.series):
            mes += "Season {}: ".format(i+1)
            for ep in flags:
                if ep:
                    mes += "✅"
                else:
                    mes += "🚫"
            mes += "\n"
        part1 = "\n".join(mes.split("\n")[:4])
        part2 = "\n".join(mes.split("\n")[4:])
        return (part1, part2)

    def watch(self, seas, ep):
        self.series[seas-1][ep-1] = True
    
    def roll(self, seas = None):
        if seas == None:
            check = [all(i) for i in self.series]
            picker = []
            for inx, i in enumerate(check):
                if not i:
                    picker.append(inx)
            if len(picker) == 0:
                return "You've watched everything..."
            seas = random.choice(picker)
        else:
            seas -= 1
            if all(self.series[seas]):
                return "You've watched everything... In this season. there are many more to try!!!!!!!"
        
        picker = []
        for inx, i in enumerate(self.series[seas]):
            if not i:
                picker.append(inx)
        
        return (seas+1, random.choice(picker)+1)
    
    def putWatcher(self):
        try:
            with open("watcher.txt", "w") as f:
                lines = ""
                for seas in self.series:
                    line = ""
                    for ep in seas:
                        line += "{};".format(int(ep))
                    line = line[:-1]
                    line += "\n"
                    lines += line
                lines = lines[:-1]
                f.write(lines)
        except Exception as e:
            print(e)
            print("Can't open file to save watcher... Rip your session...")

    def getWatcher(self):
        l = self.series.copy()
        try:
            with open("watcher.txt", "r") as f:
                for i in range(9):
                    line = f.readline()
                    nums = [bool(int(q)) for q in line.split(";")]
                    if (i == 2 and len(nums) == 13) or (i != 2 and len(nums) == 26):
                        l[i] = nums
                    else:
                        raise Exception("Invalid length of line %d" % i+1)
        except Exception as e:
            print(e)
            print("Can't open file to read watcher... Starting anew...")
            return
        self.series = l
        




if __name__ == "__main__":
    w = WatchTimeHolder()
    print(w.series)
    print(w.craftMessage())