class GST(object):
    def __init__(self, tokens1, tokens2, MML = 3):
        self.tokens1 = tokens1
        self.tokens2 = tokens2
        self.MML = MML
        self.tiles = []
        
    def match(self):
        self.tiles = []
        len1 = len(self.tokens1)
        len2 = len(self.tokens2)

        mark1 = [0] * len1
        mark2 = [0] * len2

        maxlen = 0
        while maxlen != self.MML:
            matches = []
            maxlen = self.MML
            for i in range(len1):
                if mark1[i] == 1:
                    continue
                for j in range(len2):
                    if mark2[j] == 1:
                        continue
                    count = 0
                    while i + count < len1 and j + count < len2 and self.tokens1[i+count] == self.tokens2[j+count] and mark1[i+count] != 1 and mark2[j+count] != 1:
                        count += 1
                    if count == maxlen:
                        matches.append((i, j, count))
                    elif count > maxlen:
                        matches = []
                        matches.append((i, j, count))
                        maxlen = count
            
            for m in matches:
                if 1 in mark1[m[0]:m[0]+m[2]] or 1 in mark2[m[1]:m[1]+m[2]]:
                    continue
                mark1[m[0]:m[0]+m[2]] = [1] * m[2]
                mark2[m[1]:m[1]+m[2]] = [1] * m[2]
                self.tiles.append(m)
    
    def get_tiles(self):
        return self.tiles
    
    @property
    def similarity(self):
        if len(self.tokens1) + len(self.tokens2) == 0:
            return 0
        length = 0
        for tile in self.tiles:
            length += tile[2]
        return (2.0 * length) / (len(self.tokens1) + len(self.tokens2))
