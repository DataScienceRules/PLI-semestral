

def bigram_smooting_witten_bell(bigram, newbigram):
    Nw = 0 #pocet vyskytu vsech dvojic s predchudcem w  pocet vsech trojic s predchudci w1 a w2
    Tw = 0 #pocet vsech ruznych dvojic slov s predchudcem w, ktere se objevily v datech     pocet vsech ruznych trojic s predchudci w1 a w2, ktere se objevily v datech
    Zw = 0 #pocet vsech ruznych dvojic slov s predchudcem w, ktere se neobjevily v datech   pocet vsech ruznych trojic s predchudci w1 a w2, ktere se neobjevili v datech
    cw = 0

    for idx, row in enumerate(newbigram):
        cetrow = bigram[idx]
        Nw = sum(cetrow.values())
        Tw = 0
        Zw = 0
        if Nw == 0:
            pass
        else:
            for key, value in cetrow.items():
                    if value != 0:
                        Tw += 1
                    elif value == 0:
                        Zw += 1

            # pro dvojici s pravdepodobnosti > 0:
            for key, value in cetrow.items():
                if value != 0:
                    pwb2 = value / (Nw + Tw)
                    row[key] = pwb2
            # pro dvojici s pravdepodobnosti 0:
            if Nw == 0:
                pass
            elif Nw > 0:
                pwb = Tw / (Zw * (Tw + Nw))
                for key, value in row.items():
                    if value == 0:
                        smoothed = {key: pwb}
                        row.update(smoothed)
    for row in bigram:
        print(row)
        #print(sum(row.values()))

    for row in newbigram:
        print(row)
        #print(sum(row.values()))
    return bigram, newbigram


def trigram_smooting_witten_bell(trigram, newtrigram):
    Nw = 0 #pocet vsech trojic s predchudci w1 a w2
    Tw = 0 #pocet vsech ruznych trojic s predchudci w1 a w2, ktere se objevily v datech
    Zw = 0 #pocet vsech ruznych trojic s predchudci w1 a w2, ktere se neobjevily v datech
    cw = 0
    for idex, sublist in enumerate(newtrigram):
        for idx, row in enumerate(sublist):
            cetrow = trigram[idex][idx]
            Nw = sum(cetrow.values())
            Tw = 0
            Zw = 0
            if Nw == 0:
                pass
            else:
                for key, value in cetrow.items():
                        if value != 0:
                            Tw += 1
                        elif value == 0:
                            Zw += 1

                # pro dvojici s pravdepodobnosti > 0:
                for key, value in cetrow.items():
                    if value != 0:
                        pwb2 = value / (Nw + Tw)
                        row[key] = pwb2
                # pro dvojici s pravdepodobnosti 0:
                if Nw == 0 or Zw == 0:
                    pass
                elif Nw > 0:
                    pwb = Tw / (Zw * (Tw + Nw))
                    for key, value in row.items():
                        if value == 0:
                            smoothed = {key: pwb}
                            row.update(smoothed)
    #print(trigram[0])
    #print(sum(row.values()))
    #print(newtrigram[0])
    #print(sum(row.values()))
    return trigram, newtrigram
