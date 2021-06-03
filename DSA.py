import random
import math
import string
import warnings
import sys, os
import sha3
import pyprimes
from _pysha3 import sha3_256
#
small_primes = [2, 3, 5, 7, 11, 13]

def BasicTest(n, q, k):
    a = random.randint(2, n-1)
    x = pow(a, q, n)
    if x == 1 or x == n-1:
            return 1
    for i in range(1, k):
        x = pow(x,2,n)
        if x == 1:
            return -1
        if x == n-1:
            return 1
    return -1

def MRTest(n, t):
    k = 0
    q = n-1
    while (q%2==0):
        q = q//2
        k+=1
    while (t>0):
        t = t-1
        if BasicTest(n, q, k)==1:
            continue
        else:
            return -1
    return 1

def PrimalityTest(n,t):
    for i in small_primes:
        if n%i==0:
            return -1
    else:
        MRTest(n, t)


    result = -1
    while (result == -1):
        n = random.randint(3, 2**512)
        result = MRTest(n,10)

      #  print ("n: ", n)

alphabet = "ABCDEFGHIJKLMNOPRSTUVYZXQW0123456789"
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def isprime(n):
    '''check if integer n is a prime'''
    # make sure n is a positive integer
    n = abs(int(n))
    # 0 and 1 are not primes
    if n < 2:
        return False
    # 2 is the only even prime number
    if n == 2:
        return True
    # all other even numbers are not primes
    if not n & 1:
        return False
    # range starts with 3 and only needs to go up the squareroot of n
    # for all odd numbers
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True

def isPrime(n, k=5): # miller-rabin
    from random import randint
    if n < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0: return n == p
    s, d = 0, n-1
    while d % 2 == 0:
        s, d = s+1, d//2
    for i in range(k):
        x = pow(randint(2, n-1), d, n)
        if x == 1 or x == n-1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return False
            if x == n-1: break
        else: return False
    return True
def DL_Param_Generator(small_bound, large_bound):
    q = 4 # Composite number chosen for initalizing.
    p = 4
    small_bound = 256
    large_bound = 2048
    q = random.getrandbits(256)
    count = 0
    while count< 20 :
        if  pyprimes.isprime(q):
            count += 1
        else:
            q = random.getrandbits(256)
            count = 0
    k = random.getrandbits(2048-256)
    p = k*q+1
    while not pyprimes.isprime(p):
        k = random.getrandbits(2048-256)
        #print str(k)
        p = k * q + 1

    #print'over'

    #Now we have prime numbers p and q where q divides p-1.
    #   #To choose a generator
    alpha = random.randint(1,3000)
    g = 1
    while g == 1:
        print(g)
        g = pow(alpha,(p-1)//q,p)
    file = open("DSA_params.txt", 'w')
    file.write(str(q) + "\n" + str(p) + "\n" + str(g))
    file.close()
    return q, p, g
def KeyGen(p,q,g):
    #Compute secret alpha
    alpha = random.randint(1,q-1)
    #Compute secret beta
    beta = pow(g,alpha,p)
    file1 = open("DSA_skey.txt", 'w')
    file1.write(str(q) + "\n" + str(p) + "\n" + str(g) + "/n" +str(alpha))
    file1.close()
    file2 = open("DSA_pkey.txt", 'w')
    file2.write(str(q) + "\n" + str(p) + "\n" + str(g) + "/n" +str(beta))
    file2.close()
    return alpha, beta

def SignGen(m, p, q, g, alpha, beta):
    #m = m.encode('utf-8')
    h = sha3.sha3_256(m).hexdigest()
    h = int(h, 16)
    print("SignGen: " + str(h))
    h = h % q
    k = random.randint(1, q - 1)
    r = pow(g, k, p)
    print("r " + str(r))
    s = (alpha* r + k * h) % q
    print("s " + str(s))
    return r, s  # Return signature for m which are r and s.

def SignVer(m, r, s, p, q, g, beta):
  # m = m.encode('utf-8')
    h = sha3.sha3_256(m).hexdigest()

    h = int(h,16)
    print( "SignGen: "+str(h) )
    h = h % q
    v = modinv(h, q) % q
    z1 = (s * v) % q
    z2 = ((q - r) * v) % q
    u = (pow(g, z1,p) * pow(beta, z2,p)) % p
    print(p)
    print(q)
    u=u%q
    r = r % q
    if r == u:
        return True
    else:
        return False
