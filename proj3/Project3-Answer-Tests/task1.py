#!/usr/bin/python
import binascii
import sys
import time
from des import *

def bit2str(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return t

def hex2bin(s):
    return s.decode('hex')

def str2bit(s):
    bitArray = []
    for i in s:
        temp = str(bin(ord(i)))[2:]
        if len(temp) != 8:
            bitArray.extend([0] * (8 - len(temp)))
        for j in temp:
            bitArray.append(int(j))

    return bitArray

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

    #print bintohex("".join([str(e) for e in c]))

def cbc_encrypt(message, key, iv):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      ciphertext: string
    """
    # TODO: Add your code here.
    #test()


    # do padding
    numBytes = len(message)

    if numBytes % 8 != 0:
        # message[-1] += 1
        # message[-1] << (8 - (len(bin(ord(message[-1]))) - 2))
	print numBytes
	message += chr(2**7)
        message += "\0" * (7 - numBytes % 8)
    else:
        message += chr(2**7) + "\0" * 7
    

    result = ""

    key = hex2bin(key.strip())
    iv = hex2bin(iv.strip())
    k = des(key)

    for i in range(0, len(message), 8):
        plaintext = message[i:i+8]

        # IV XOR Plaintext
        temp = ""
        for j in range(0, 8):
            temp += chr(ord(plaintext[j]) ^ ord(iv[j]))

        c = k.des_encrypt(str2bit(temp))
	# The following two lines are for debugging.
	s = "".join([str(e) for e in c])
	print "".join([hex(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8)])

        ciphertext = bit2str("".join([str(e) for e in c]))
	print "".join([str(e) for e in c])
        iv = ciphertext
        result += ciphertext
    
    return result


def cbc_decrypt(message, key, iv):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      plaintext: string
    """

    result = ""
    key = hex2bin(key.strip())
    iv = hex2bin(iv.strip())
    k = des(key)

    for i in range(0, len(message), 8):
        ciphertext = message[i:i+8]

        p = k.des_decrypt(str2bit(ciphertext))
        temp = bit2str("".join([str(e) for e in p]))

        # IV XOR Plaintext
        plaintext = ""
        for j in range(0, 8):
            plaintext += chr(ord(temp[j]) ^ ord(iv[j]))

        iv = ciphertext

        result += plaintext

    bits = str2bit(result)
    for i in range(len(bits) - 1, -1, -1):
        if bits[i] == 1:
            break
    return result[:i/8]


def main(argv):
    if len(argv) != 5:
        print 'Wrong number of arguments!\npython task1.py $MODE $INFILE $KEYFILE $IVFILE $OUTFILE'
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
        print 'File Not Found'
    start = time.time()
    if mode == "enc":
        output = cbc_encrypt(message, key, iv)
    elif mode == "dec":
        output = cbc_decrypt(message, key, iv)
    else:
        print "Wrong mode!"
        sys.exit(1)
    end = time.time()
    print "Consumed time=", (end - start)
    open(outfile, 'w').write(output)

if __name__=="__main__":
    main(sys.argv[1:])
