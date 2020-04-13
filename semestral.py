from tkinter import filedialog
import tkinter as tk
from venv.smoothing_WB import bigram_smooting_witten_bell, trigram_smooting_witten_bell
from numpy import prod
from venv import WikiExtractor
import os, json, re, unicodedata
from math import log

alphabet = [" ", ".", ",", "a", "ä", "á", "b", "c", 'č', "d", "ď", "e", "é", "ě", "f", "g", "h", "i", "í", "j", "k", "l", "ĺ", "ľ", "ô", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř", "ŕ", "s", "š", "t", "ť", "u", "ú", "ů", "v", "w", "x", "y", "ý", "z", "ž"]
reduced_alphabet = [" ", ".", ",", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
apriorni_prst = 0.5

def open_new_text():
    filename = filedialog.askopenfilename(title="Select file", filetypes=(("text files", "txt"),))
    #filename = ""
    print("Opening: " + filename)
    file = open(filename, mode="r", buffering=1, encoding="utf-8")
    return file


def prepare_line(line):
    line = line.lower()
    line.rstrip('\n')
    line = re.sub('[":)(!@#$°„“-]', '', line)
    line = re.sub('\n', '', line)

    line = re.sub(' formula_\d*|\d*', '', line)
    line = re.sub('formula', '', line)
    clean_tags = re.compile('<.*?>')
    line = re.sub(clean_tags, "", line)
    line = re.sub('[^ ,.aäábcčdďeéěfghiíjklĺľômnňoópqrřŕsštťuúůvwxyýzž]', '', line)
    line = re.sub('\s{2,}', ' ', line)
    line = re.sub('\s*[.]', '.', line)

    return line


def prepare_reduced_line(line):
    line = line.lower()
    line.rstrip('\n')
    line = re.sub('[":)(!@#$°„“-]', '', line)
    line = re.sub('\n', '', line)

    line = re.sub(' formula_\d*|\d*', '', line)
    line = re.sub('formula', '', line)
    clean_tags = re.compile('<.*?>')
    line = re.sub(clean_tags, "", line)
    line = re.sub('[^ ,.aäábcčdďeéěfghiíjklĺľômnňoópqrřŕsštťuúůvwxyýzž]', '', line)
    line = re.sub('\s{2,}', ' ', line)
    line = re.sub('\s*[.]', '.', line)
    line = unicodedata.normalize('NFD', line).encode('ascii', 'ignore').decode("utf-8")

    return line


def fill_all_zeros_lines(newtrigram):
    for sublist in newtrigram:
        for slicelist in sublist:
            values = slicelist.values()
            if all(flag == 0 for flag in values) is True:

                for x in slicelist.keys():
                    slicelist[x] = 1
    return newtrigram


def create_unigram(filelist):
    unigram = {}
    for char in filelist:
        if char in unigram:
            unigram[char] += 1
        elif char not in unigram:
            unigram[char] = 1

    unigram = {k: v / len(filelist) for k, v in unigram.items()}
    for char in alphabet:
        if char not in unigram:
            unigram[char] = 0
    print(unigram)


def create_bigram(filelist):
    bigram = []

    """ \

    [{"aa": 0, "ab": 0, "ac": 0, ...},
     {"ba": 0, "bb": 0, "bc": 0, ...},
      ...
    ]
    """
    for char in alphabet:
        subdict = {}
        for cha in alphabet:
            subdict[char+cha] = 0
        bigram.append(subdict)

    for idex, char in enumerate(filelist):
        if idex == 0:
            pass
        else:
            bigram_key = char+filelist[idex-1]
            bigram_line = alphabet.index(char)
            bigram[bigram_line][bigram_key] += 1

    newbigram = []
    for row in bigram:
        divider = sum(row.values())
        newrow = {}
        for key, val in row.items():
            if divider == 0:
                pass
            elif divider > 0:
                val = val / divider
            newrow[key] = val
        #row = {k: v / divider for k, v in row.items()}
        newbigram.append(newrow)

    return bigram, newbigram


def create_trigram(file):
    trigram = []
    """ \
    [
        [{"aaa": 0, "aab": 0, "aac": 0, ...},
         {"aba": 0, "abb": 0, "abc": 0, ...},
          ...
        ],
        [{"baa": 0, "bab": 0, "bac": 0, ...},
         {"bba": 0, "bbb": 0, "bbc": 0, ...},
          ...
        ],
        [{"caa": 0, "cab": 0, "cac": 0, ...},
         {"cba": 0, "cbb": 0, "cbc": 0, ...},
          ...
        ]
        ...
    ]
    """
    for char in reduced_alphabet:
        subfield = []
        for cha in reduced_alphabet:
            sublist = {}
            for ch in reduced_alphabet:
                sublist[char+cha+ch] = 0
            subfield.append(sublist)
        trigram.append(subfield)

    lasttwo = ''
    for idx, line in enumerate(file):
        if idx < 0:
            line = prepare_reduced_line(line)
            line = lasttwo+line
        else:
            line = prepare_reduced_line(line)
        lasttwo = line[-2:]+' '

        for ide, character in enumerate(line):
            if ide < 2:
                pass
            else:
                trigram_key = character+line[ide-1]+line[ide-2]
                trigram_list = reduced_alphabet.index(character)
                trigram_dict = reduced_alphabet.index(line[ide-1])
                trigram[trigram_list][trigram_dict][trigram_key] += 1

    #trigram = fill_all_zeros_lines(trigram)

    newtrigram = []
    for sublist in trigram:
        newsublist = []
        for row in sublist:
            divider = sum(row.values())
            newrow = {}
            for key, val in row.items():
                if divider == 0:
                    pass
                elif divider > 0:
                    val = val / divider
                newrow[key] = val
            newsublist.append(newrow)
        newtrigram.append(newsublist)
    return trigram, newtrigram


def create_trained_trigram_file(trigram, language):
    name = language+"trainedtrigram.txt"
    with open(name, "w", encoding="utf-8") as outfile:
        json.dump(trigram, outfile)


def open_trained_trigram_file():
    filename = filedialog.askopenfilename(title="Select file", filetypes=(("text files", "txt"),))
    # filename = ""
    print("Opening: " + filename)
    file = open(filename, mode="r", buffering=1, encoding="utf-8")
    file = json.loads(file.read())
    return file


def bayes(trained_trigram, testing_trigram):
    trigramprst = []
    for idx, sublist in enumerate(testing_trigram):
        sliceprst = []
        for idex, row in enumerate(sublist):
            rowprst = []
            for k, v in row.items():
                if v == 0:
                    pass
                elif v > 0:
                    firstidx = reduced_alphabet.index(k[0])
                    secondidx = reduced_alphabet.index(k[1])
                    onekeyprst = -log(trained_trigram[firstidx][secondidx][k] * v)
                    rowprst.append(onekeyprst)
            rowprst = npsum(rowprst)
            sliceprst.append(rowprst)
        sliceprst = npsum(sliceprst)
        trigramprst.append(sliceprst)
    resultprst = npsum(trigramprst) * apriorni_prst
    return resultprst


#create_unigram(split_file(open_new_text()))
#bigram, newbigram = create_bigram(split_file(open_new_text()))
#trigram, newtrigram = create_trigram(split_file(open_new_text()))

#bigram_smooting_witten_bell(bigram, newbigram)
#trigram, newtrigram = trigram_smooting_witten_bell(trigram, newtrigram)
#print("testing", trigram[0])
#print("trained", newtrigram[0])
#create_trained_trigram_file(newtrigram, "CZtest")
#print(bayes(newtrigram, trigram))
#print(open_trained_trigram_file())

'''
cz = open_new_text()
sk = open_new_text()
cztrigram, cznewtrigram = create_trigram(cz)
cztrigram, cznewtrigram = trigram_smooting_witten_bell(cztrigram, cznewtrigram)
create_trained_trigram_file(cznewtrigram, "CZreduced")

sktrigram, sknewtrigram = create_trigram(sk)
sktrigram, sknewtrigram = trigram_smooting_witten_bell(sktrigram, sknewtrigram)
create_trained_trigram_file(sknewtrigram, "SKreduced")
'''


cet, prst = create_trigram(open_new_text())
print(bayes(open_trained_trigram_file(), cet))
print(bayes(open_trained_trigram_file(), cet))





