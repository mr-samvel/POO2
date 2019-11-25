def stonks(mediam, opens, closes, datas, num):
    tupl = []
    for i in range(len(closes)-6, len(closes)):
        if mediam[num][i] <= opens[num][i] or mediam[num][i] >= closes[num][i]:
            if mediam[num[i]] > opens[num][i+5]:
                tupl.append(tuple ([datas[num][i], mediam[num][i], 1]))
            else:
                tupl.append(tuple ([datas[num][i], mediam[num][i], 0]))
        else:
            tupl.append(tuple ([datas[num][i], mediam[num][i], 2]))
    return tupl
