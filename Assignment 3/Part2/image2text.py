#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!

def data_reading(fname):
    data_arr = []
    file = open(fname,'r')
    for sentence in file:
        info = tuple([x for x in sentence.split()])
        
        data_arr += [(info[0::2], info[1::2]),]
    
    return data_arr

alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

trans_count = {}
trans_prob = {}
data = data_reading(train_txt_fname)
alpha = 1.2

for phrases, speech in data:
    for word in phrases:

        prev = " "
        for alphabet in word :
            if alphabet not in trans_count:
                trans_count[alphabet] = {}
                trans_prob[alphabet] = {}
                trans_count[alphabet][prev] = 1
                trans_prob[alphabet][prev] = 1
            else:
                if prev not in trans_count[alphabet]:
                    trans_count[alphabet][prev] = 1
                else:
                    trans_count[alphabet][prev] += 1
                trans_prob[alphabet][prev] = 1

            prev = alphabet
#print(trans_count)
for alphabet in trans_count:        
    complete_count = sum(trans_count[alphabet].values())
    for before in trans_count[alphabet]:
        trans_prob[alphabet][before] = math.log(float(trans_count[alphabet][before])/float(complete_count))*alpha

def emission_prob(test_alphabet,alphabet):
    emi_prob = 0

    for i in range(len(test_alphabet)):
        for j in range(len(test_alphabet[i])):
            if train_letters[alphabet][i][j] == test_alphabet[i][j] and test_alphabet[i][j] == '*':
                emi_prob += math.log(0.95)
            elif train_letters[alphabet][i][j] == test_alphabet[i][j] and test_alphabet[i][j] == ' ':
                emi_prob += math.log(0.65)
            elif train_letters[alphabet][i][j] != test_alphabet[i][j] and test_alphabet[i][j] == ' ':
                emi_prob += math.log(0.35)
            else:
                emi_prob += math.log(0.05)
    #print(emi_prob)
    return emi_prob

# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:

#trans_prob[" "][" "] = math.log(1e-200)*alpha

basic = ''
for i in range(len(test_letters)):
    alpha_maxx = 'A'
    prob_maxx = -1000
    for alphabet in alphabets:
        e_prob = emission_prob(test_letters[i],alphabet)
        if e_prob > prob_maxx:
            alpha_maxx = alphabet
            prob_maxx = e_prob
    basic += alpha_maxx

mat = [[(0,'A') for i in range(72)] for j in range(len(test_letters))]

m = 0
for alphabet in alphabets:
    if alphabet in trans_prob:
        t = trans_prob[alphabet][" "]*alpha
        e = emission_prob(test_letters[0],alphabet)
        mat[0][m] = (t+e,alphabet)

    elif alphabet.lower() in trans_prob:
        t = trans_prob[alphabet.lower()][" "]*alpha
        e = emission_prob(test_letters[0],alphabet)
        mat[0][m] = (t+e,alphabet)

    else:
        mat[0][m] = (math.log(1e-200)*alpha , alphabet)
    m += 1

for i in range(1,len(test_letters)):
    for j in range(len(alphabets)):
        prob_max = -100000
        prev = 'A'
        for k in range(len(alphabets)):
            if alphabets[j] in trans_prob:
                if alphabets[k] in trans_prob[alphabets[j]]:
                    hm = trans_prob[alphabets[j]][alphabets[k]]*alpha
            elif alphabets[j].lower() in trans_prob:
                if alphabets[k] in trans_prob[alphabets[j].lower()]:
                    hm = trans_prob[alphabets[j].lower()][alphabets[k]]*alpha
            else:
                hm = math.log(1e-200)*alpha
            
            if mat[i-1][k][0] + hm > prob_max:
                prob_max = mat[i-1][k][0] + hm
                prev = mat[i-1][k][1]

        ans = prev + alphabets[j]
        mat[i][j] = (prob_max + emission_prob(test_letters[i],alphabets[j]),ans)
    

maxx = -100000
final_res = ''
res = ''
p = 0
n = len(test_letters)
for j in range(len(alphabets)):
    if mat[n-1][j][0] > maxx:
        final_res = alphabets[j]
        res = final_res
        p = j

sentence = mat[n-1][p][1]


# The final two lines of your output should look something like this:
print("Simple: " , basic)
print("   HMM: " + sentence) 


