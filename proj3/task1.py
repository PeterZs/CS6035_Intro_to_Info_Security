#!/usr/bin/python
import binascii
import sys
import time
from des import *

def bintohex(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return binascii.hexlify(t).upper()

def test():
    key1 = b"\0\0\0\0\0\0\0\0"
    key2 = b"\0\0\0\0\0\0\0\2"
    message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    message2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    test_des(key1, message1)
    test_des(key1, message2)
    test_des(key2, message1)
    test_des(key2, message2)

def test_des(key, message):
    k = des(key)
    c = k.des_encrypt(message)
    print (bintohex("".join([str(e) for e in c])))

def cbc_encrypt(message, key, iv):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      ciphertext: string
    """
    # TODO: Add your code here.
    key_string = binascii.unhexlify(key)

    iv_bin = bin(int(iv, 16))[2:]
    message_bin = bin(int(binascii.hexlify(message), 16))




    if len(message_bin) % 64 == 0:
        pass
    else:
        padding_length = 64 - (len(message_bin) % 64)
        if padding_length == 1:
            message_bin += '1'
        else:
            message_bin += '1'
            while (64 - (len(message_bin) % 64)) < 64:
                message_bin += '0'

    message_bin = message_bin[0] + message_bin[2:] + '0'

    plaintextlist = [message_bin[0+i:64+i] for i in range(0, len(message_bin), 64)]
    block_xor = '{0:0{1}b}'.format(int(plaintextlist[0], 2) ^ int(iv_bin, 2), len(plaintextlist[0]))
    block_xor = list(block_xor)
    block_xor = [int(x) for x in block_xor]
    k = des(key_string)
    cipherstring = k.des_encrypt(block_xor)
    cipherbin_list = [''.join(str(x) for x in cipherstring)]
    ciper_list = [cipherstring]

    for i in range(1, len(plaintextlist)):

        chain_block_xor = '{0:0{1}b}'.format(int(plaintextlist[i], 2) ^ int(cipherbin_list[i-1], 2), len(plaintextlist[i]))
        chain_block_xor = list(chain_block_xor)

        chain_block_xor = [int(x) for x in chain_block_xor]


        cipherstring = k.des_encrypt(chain_block_xor)

        cipherbin_list.append(''.join(str(x) for x in cipherstring))

        ciper_list.append(cipherstring)




    cipher_bin_string = ''.join(str(x) for y in ciper_list for x in y)




    chars = []
    for i in range(len(cipher_bin_string) / 8):
        byte = cipher_bin_string[i*8:(i+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def cbc_decrypt(message, key, iv):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      plaintext: string
    """
    # TODO: Add your code here.
    buffer = []
    for c in message:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        buffer.extend([int(b) for b in bits])

    message_binary = buffer
    key_string = binascii.unhexlify(key)
    iv_bin = bin(int(iv, 16))[2:]
    cipher_list = [message_binary[0+i:64+i] for i in range(0, len(message_binary), 64)]

    k = des(key_string)
    des1 = k.des_decrypt(cipher_list[0])
    des1 = ''.join(str(x) for x in des1)
    iv_dec1_xor = '{0:0{1}b}'.format(int(des1, 2) ^ int(iv_bin, 2), len(des1))

    plaintext = iv_dec1_xor




    for i in range(1, len(cipher_list)):
        decripttext_list = k.des_decrypt(cipher_list[i])
        decripttext = ''.join(str(x) for x in decripttext_list)
        cipherblock = ''.join(str(x) for x in cipher_list[i-1])
        cipher_xor = '{0:0{1}b}'.format(int(decripttext, 2) ^ int(cipherblock, 2), len(decripttext))
        plaintext += cipher_xor

    plaintext = plaintext[::-1]
    j = 0
    while plaintext[j] == '0':
        pass
        j += 1
    j += 1

    plaintext = plaintext[j:][::-1]
    chars = []
    for i in range(len(plaintext) / 8):
        byte = plaintext[i*8:(i+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)



def main(argv):
    if len(argv) != 5:
        print ('Wrong number of arguments!\npython task1.py $MODE $INFILE $KEYFILE $IVFILE $OUTFILE')
        sys.exit(1)
    mode = argv[0]
    infile = argv[1]
    keyfile = argv[2]
    ivfile = argv[3]
    outfile = argv[4]
    message = None
    key = None
    iv = None
    try:
        message = open(infile, 'r').read()
        key = open(keyfile, 'r').read()
        iv = open(ivfile, 'r').read()
    except:
        print ('File Not Found')
    start = time.time()
    if mode == "enc":
        output = cbc_encrypt(message, key, iv)
    elif mode == "dec":
        output = cbc_decrypt(message, key, iv)
    else:
        print ("Wrong mode!")
        sys.exit(1)
    end = time.time()
    print ("Consumed CPU time=%f"% (end - start))
    open(outfile, 'w').write(output)

if __name__=="__main__":
    main(sys.argv[1:])
