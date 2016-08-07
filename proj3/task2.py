#!/usr/bin/python

import sys
import des_wrapper
import time
import binascii

def bit2byte(bitdata):
    result = []
    for i in range(len(bitdata) / 8):
        byte = bitdata[i * 8:(i + 1) * 8]
        result.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(result)

def generatekey(removedparity):

    current_num = removedparity

    current_bin = bin(current_num)[2:]

    if len(current_bin) % 56 == 0:
        padding = 0
    else:
        padding = 56 - (len(current_bin) % 56)
    current_bin = padding*'0' + bin(current_num)[2:]

    current_blocks = [current_bin[0+i:7+i] for i in range(0, len(current_bin), 7)]

    for i in range(len(current_blocks)):
        numofones = 0
        for character in current_blocks[i]:
            if character == '1':
                numofones += 1
        if numofones % 2 == 0:
            current_blocks[i] = '1' + current_blocks[i]
        else:
            current_blocks[i] = '0' + current_blocks[i]





    addparity_bin = ''.join(str(i) for i in current_blocks)
    #print "addparity_bin = ", addparity_bin

    hex_current = hex(int(addparity_bin, 2))
    #print "hex_current =", hex_current
    if hex_current[-1] == 'L':
        hex_current = hex_current[2:-1]
    else:
        hex_current = hex_current[2:]
    if len(hex_current) == 15:
        hex_current = '0' + hex_current
    keylist = [int(x) for x in addparity_bin]
    return keylist

def enum_key(current):
    """Return the next key based on the current key as hex string.

    TODO: Implement the required functions.
    """
    current_bin = bin(int(current, 16))[2:]
    #print "current_bin =", current_bin
    #print "current_bin length =", len(current_bin)
    if len(current_bin)<64:
        current_bin = (64-len(current_bin))*'0' + current_bin

    currentbinary_blocks = [current_bin[0+i:8+i] for i in range(0, len(current_bin), 8)]
    #print "currentbinary_blocks =", currentbinary_blocks

    for i in range(len(currentbinary_blocks)):
        currentbinary_blocks[i] = currentbinary_blocks[i][1:]
    #print "len(currentbinary_blocks[6]) = ", len(currentbinary_blocks[6])
    removedparity_bin = ''.join(str(i) for i in currentbinary_blocks)
    #print "removedparity_bin =", removedparity_bin
    #print "length of removed binary =",len(removedparity_bin)
    removedparity_num = int(removedparity_bin, 2)
    #print "removedparity_num =", removedparity_num
    next_num = removedparity_num + 1

    next_bin = bin(next_num)[2:]

    if len(next_bin) % 56 == 0:
        padding = 0
    else:
        padding = 56 - (len(next_bin) % 56)
    next_bin = padding*'0' + bin(next_num)[2:]
    #print 'padding = ',padding
    #next_bin =bin(next_num)[2:]
    #print "next_bin =", next_bin
    next_num_blocks = [next_bin[0+i:7+i] for i in range(0, len(next_bin), 7)]
    #print "next_num_blocks = ", next_num_blocks
    for i in range(len(next_num_blocks)):
        numofones = 0
        for character in next_num_blocks[i]:
            if character == '1':
                numofones += 1
        if numofones % 2 == 0:
            next_num_blocks[i] = '1' + next_num_blocks[i]
        else:
            next_num_blocks[i] = '0' + next_num_blocks[i]

    addparity_bin = ''.join(str(i) for i in next_num_blocks)
    hex_next = hex(int(addparity_bin, 2))
    #print "hex_next =", hex_next
    if hex_next[-1] == 'L':
        hex_next = hex_next[2:-1]
    else:
        hex_next = hex_next[2:]
    if len(hex_next) == 15:
        hex_next = '0' + hex_next
    return hex_next

def main(argv):
    if argv[0] == 'enum_key':
        print (enum_key(argv[1]))
    elif argv[0] == 'crack':
        """TODO: Add your own code and do whatever you do.
        """
        plaintext = open('plaintext', 'r').read()
        print "plaintext = ", plaintext
        plaintext_bin = '0' + bin(int(binascii.hexlify(plaintext), 16))[2:]
        plaintext_list = [int(x) for x in plaintext_bin]
        ciphertext = open('ciphertext', 'r').read()
        keyrange = ['808080C180808080','808080C17F7F7F7F']
        start_bin = bin(int(keyrange[0], 16))[2:]
        if len(start_bin)<64:
            start_bin = (64-len(start_bin))*'0' + start_bin
        end_bin = bin(int(keyrange[1], 16))[2:]
        if len(end_bin)<64:
             end_bin = (64-len( end_bin))*'0' +  end_bin

        startbin_blocks = [start_bin[0+i:8+i] for i in range(0, len(start_bin), 8)]
        endbin_blocks = [end_bin[0+i:8+i] for i in range(0, len(end_bin), 8)]

        for i in range(len(startbin_blocks)):
            startbin_blocks[i] = startbin_blocks[i][1:]

        for i in range(len(endbin_blocks)):
            endbin_blocks[i] = endbin_blocks[i][1:]

        start_rmparity_bin = ''.join(str(i) for i in startbin_blocks)
        #print "length of start_rmparity_bin = ", len(start_rmparity_bin)

        start = int(start_rmparity_bin, 2)
        #print "start = ", start

        end_rmparity_bin = ''.join(str(i) for i in endbin_blocks)
        #print "length of end_rmparity_bin = ", len(end_rmparity_bin)

        end = int(end_rmparity_bin, 2)
        print end-start
        begintime = time.time()

        while start <= end:
            #to_hex = hex(start)[2:len(hex(start))-1]
            #key = bin(int(enum_key(to_hex), 16))[2:]
            #keylist = [int(x) for x in key]
            keylist = generatekey(start)
            decrypttext = bit2byte(des_wrapper.des_encrypt(keylist, plaintext_list))
            #print decrypttext
            if decrypttext == ciphertext:
                print 'key found'
                break
            start +=1
            #print "start = ",start
        endtime = time.time()
        print "time difference is = ", endtime - begintime
    else:
        raise Exception("Wrong mode!")

if __name__=="__main__":
    main(sys.argv[1:])
