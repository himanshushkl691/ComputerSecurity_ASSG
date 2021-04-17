#!/usr/bin/env python3
from hashlib import md5
import random
import time
import math


def computeMD5Hash(data):
    return md5(data.encode('utf-8')).hexdigest()


def getBinary(data, base, reqBits=128):
    data = str(data)
    return bin(int(data, base))[2:].zfill(reqBits)


def MD5Digest(data, bits=128):
    hash = computeMD5Hash(data)
    return getBinary(hash, 16, 128)[0:bits]


def newText(data, infoBits):
    listData = list(data)
    listInfoBits = list(infoBits)
    infoBitsLen = len(listInfoBits)
    for i in range(0, infoBitsLen):
        if listInfoBits[i] == '1':
            if listData[i] == '0':
                listData[i] = '1'
            else:
                listData[i] = '0'
    return "".join(listData)


def collision(data, bits):
    hashData = MD5Digest(data, bits)
    guess = 1
    x = newText(data, getBinary(random.randint(1, 1 << 256), 10, 256))
    while x == data or MD5Digest(x, bits) != hashData:
        x = newText(data, getBinary(random.randint(1, 1 << 256), 10, 256))
        guess = guess + 1
    return guess


bits = 2
a = getBinary(random.randint(0, 1 << 256), 10, 256)
while bits <= 128:
    totalTime = 0
    totalGuesses = 0
    for i in range(0, 1000):
        start = time.time()
        guess = collision(a, bits)
        end = time.time()
        print(end - start)
        totalGuesses = totalGuesses + guess
        totalTime = totalTime + (end - start)
    file = open("Result_" + str(bits) + "bits.txt", "w")
    file.write('Message Digest bits :%d, Average time required:%0.10f s and average guesses:%d' %
               (bits, totalTime / 1000, math.ceil(totalGuesses / 1000)))
    print('Bits %d done!' % (bits))
    bits = bits * 2
    file.close()
