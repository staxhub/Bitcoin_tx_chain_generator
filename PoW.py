import random
import pyprimes
import hashlib
import sys, os
import sha3
import TxBlockGen

def PoW(TxBlockFile, ChainFile, PoWLeN, TxLen):
    if os.path.exists(ChainFile):
        cFile = open(ChainFile, "r")
        chainFile = cFile.read().splitlines()
        cFile.close()
        print "chainFile is "
        print chainFile
    else:
        chainFile = ""
    cFile = open(ChainFile, "w")
    TxCount = 8
    LinkLen = 4
    if len(chainFile) == 0:
        PrevHash = "Day Zero Link in the Chain"
    else:
        PrevHash = chainFile[-1]
    chainFile.append(str(PrevHash))
    # Write merkle root
    txBlockFile = open(TxBlockFile, "r")
    lines = txBlockFile.readlines()
    txBlockFile.close()
    hashTree = []
    for i in range(0, TxCount):
        transaction = "".join(lines[i * TxLen:(i + 1) * TxLen])
        hashTree.append(sha3.sha3_256(transaction).hexdigest())
    t = TxCount
    j = 0
    while (t > 1):
        for i in range(j, j + t, 2):
            hashTree.append(sha3.sha3_256(hashTree[i] + hashTree[i + 1]).hexdigest())
        j += t
        t = t >> 1
    h = hashTree[2 * TxCount - 2]
    print "merkle root is: "
    print str(h)
    chainFile.append(h)
    print "chainFile is: "
    print chainFile
    Nonce = random.getrandbits(128)
    h = ""
    transaction = []
    j = int(TxBlockFile[16:-4])
    print "block number is: " + str(j)
    for i in range(j*LinkLen, (j+1)*LinkLen-2 ):
        transaction.append(chainFile[i])
    transaction.append("dummy")
    print "Transaction is: "
    print transaction
    while h[0:PoWLeN] != "0" * PoWLeN: # Hashteki 0 sayisi
        Nonce += 1
        transaction.pop()
        transaction.append(str(Nonce))
        transactionWithNonce = "\n".join(transaction[0:LinkLen-1]) + "\n"
        print " transactionWithNonce: " + transactionWithNonce
        print "repr transactionWithNonce: " +repr(transactionWithNonce)
        h = sha3.sha3_256(transactionWithNonce).hexdigest()
        print "hash value is: " + str(h)
    chainFile.append(Nonce)
    chainFile.append(h)
    print "Final chainFile is: "
    print chainFile
    cFile.writelines(["%s\n" % s  for s in chainFile])
    cFile.close()
    #Generating the LongestChain for the transaction blocks.
PoW("TransactionBlock0.txt","LongestChain.txt",3,10) 
PoW("TransactionBlock1.txt","LongestChain.txt",3,10)
PoW("TransactionBlock2.txt","LongestChain.txt",3,10)