def GST_sim(tokens1, tokens2):
    MML = 3  # minimum match length
    titles = []
    matches = []

    len1 = len(tokens1)
    len2 = len(tokens2)

    mark1 = [0] * len1
    mark2 = [0] * len2

    maxlen = 0
    while maxlen != MML:
        matches = []
        maxlen = MML
        for i in range(len1):
            if mark1[i] == 1:
                continue
            for j in range(len2):
                if mark2[j] == 1:
                    continue

                count = 0
                while i + count < len1 and j + count < len2 and tokens1[i+count] == tokens2[j+count] and mark1[i+count] != 1 and mark2[j+count] != 1:
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
            titles.append(m)

    length = 0
    for tile in titles:
        length += tile[2]
        print(tile[0], ":", tile[0]+tile[2]-1, ", ", tile[1], ":", tile[1]+tile[2]-1)
    return (2.0 * length) / (len1 + len2)
