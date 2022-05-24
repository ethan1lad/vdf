import random

from consts import first_primes_list


# Utility function to do modular exponentiation.
# It returns (x^y) % p.
def power(x, y, p):
    res = 1  # Initialize result
    x = x % p  # Update x if it is more
    # than or equal to p
    while y > 0:
        # If y is odd, multiply x with result
        if y & 1:
            res = (res * x) % p
        # y must be even now
        y = y >> 1  # y = y/2
        x = (x * x) % p
    return res


# Returns square root if square root of n under
# modulo p exists. Assumption: p is of the
# form 3*i + 4 where i >= 1
def squareRoot(n, p):
    if p % 4 != 3:
        return
    # Try "+(n^((p + 1)/4))"
    n = n % p
    x = power(n, (p + 1) // 4, p)
    if (x * x) % p == n:
        return x
    # Try "-(n ^ ((p + 1)/4))"
    x = p - x
    if (x * x) % p == n:
        return x
    # If none of the above two work, then
    # square root doesn't exist
    return -1


def nBitRandom(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def getLowLevelPrime(n):
    '''Generate a prime candidate divisible
    by first primes'''
    while True:
        # Obtain a random number
        pc = nBitRandom(n)
        # Test divisibility by pre-generated
        # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
                break
        else:
            return pc


def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert (2 ** maxDivisionsByTwo * ec == mrc - 1)

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True


# Large Prime Generation of size n bits
def getPrime(n):
    while True:
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            print(n, "bit prime is: \n", prime_candidate)
            return prime_candidate
            break


# Generate gaussian prime of size n bits
def getGaussianPrime(n):
    p = getPrime(n)
    while p % 4 != 3:
        print("Ho")
        p = getPrime(n)
    return p


# Encode Big Int (Max size 16 Bytes)
def encodeBigInt(n):
    nAsHex = format(n, 'x')
    # Prepend with 0's to make size 16 Bytes
    if len(nAsHex) != 32:
        nAsHex = "0" * (32 - len(nAsHex)) + nAsHex
    length = format(int(len(nAsHex) / 2), 'x')
    # Ensure length takes up one byte (Should not run anyway since length should always be 32 (16 Bytes)
    if len(length) == 1:
        length = "0" + length
    return length + nAsHex


# Encode Collection of Big Ints
def encodeCollBigInt(coll):
    collLength = format(int(len(coll)),'x')
    # If length odd, prepend 0 (so that encoding takes up a whole number of bytes)
    if len(collLength) % 2 == 1:
        collLength = "0" + collLength
    # Coll Big Int type prefix + Coll Length + 01 (For VLQ encoding, assumes 0x7f < length < 0x3fff
    res = "12" + collLength + "01"
    for bInt in coll:
        res += bInt
    return res