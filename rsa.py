import numpy as np
import unittest
import math
from modulo_math import ModuloMath
import random
from itertools import count, islice
import struct
import codecs

# Voici le code Python pour int to string
# Prend un entier en paramètre et le retourne en UTF-8 (avec les accents! ;) )


def intToUtf8(m):
    m = str(hex(m)[2:])  # Prendre à partir du deuxième caractère (après le 0x)
    # Inversion des octets 0x20654A ==> 0x4A6520
    m = "".join(reversed([m[i:i+2] for i in range(0, len(m), 2)]))
    m = codecs.decode(m, "hex").decode('utf-8')  # Décodage
    return m


def is_prime(n):
    if n < 2:
        return False

    for number in islice(count(2), int(math.sqrt(n) - 1)):
        if n % number == 0:
            return False

    return True


class RSA_Key:
    def __init__(self, n, e, p, q, d):
        self.n = n
        self.e = e
        self.p = p
        self.q = q
        self.d = d

    def __str__(self):
        return f"p={self.p}, q={self.q}, n={self.n}, e={self.e}, d={self.d}"


class RSA:
    CACHED_PRIMES = []

    @staticmethod
    def cached_primes():
        if(len(RSA.CACHED_PRIMES) == 0):
            print("Computing primes")
            minPrime = 0
            maxPrime = 1000
            RSA.CACHED_PRIMES = [i for i in range(
                minPrime, maxPrime) if is_prime(i)]

        return RSA.CACHED_PRIMES

    @staticmethod
    def create_keys():
        """
        Create a random pair of public and private random RSA keys.
        """
        p = random.choice(RSA.cached_primes())
        q = random.choice(RSA.cached_primes())
        n = p * q
        phi_n = (p-1) * (q-1)

        while True:
            e = random.choice(RSA.cached_primes())
            if(ModuloMath.euclid_extended(phi_n, e)[0] == 1):
                break

        return RSA.compute_key(n, e, p, q)

    @staticmethod
    def compute_key(n, e, p, q):

        phi_n = (p-1) * (q-1)  # TODO optimize/make a function great again

        results = ModuloMath.euclid_extended(phi_n, e)
        d = results[2]
        if(d < 0):
            d += phi_n

        return RSA_Key(n, e, p, q, d)

    @staticmethod
    def brute_force(n, e):
        for p in range(2, math.ceil(math.sqrt(n))):
            #print(f"{n} % {p} == {n%p}")
            if n % p == 0:
                q = n // p
                #print(f"q = {n} // {p} == {q}")
                if ModuloMath.euclid_extended(q, p)[0] == 1:
                    return RSA.compute_key(n, e, p, q)

    @staticmethod
    def encode(M, rsa_key):
        return ModuloMath.rapid_exponentiation(M, rsa_key.e, rsa_key.n)

    @staticmethod
    def decode(u, rsa_key):
        return ModuloMath.rapid_exponentiation(u, rsa_key.d, rsa_key.n)

    @staticmethod
    def decode_list(list_u, rsa_key):
        string = ""
        for u in list_u:
            M = RSA.decode(u, rsa_key)
            string += intToUtf8(M)

        return string


class TestingRSA(unittest.TestCase):
    def test_brute_force(self):
        keys = RSA.create_keys()
        bruteForce = RSA.brute_force(keys.n, keys.e)

        self.assertTrue(np.array_equal([keys.p, keys.q].sort(), [
                        bruteForce.p, bruteForce.q].sort()))


if __name__ == '__main__':
    # unittest.main()

    # list_u = [139625027, 728808256, 677396451, 662265473, 845995352, 613303937, 1033970589, 623160996, 1160483016,
    #          243815344, 572050792, 495107014, 909878795, 367266109, 273461422, 593918599, 807072360, 1029159804,
    #          243815344, 710536598, 219532422, 339194689, 1115370236, 803893657, 806790933, 145790893, 601459052, 259270170, 120667892, 994450868, 456798524, 411559218, 1033648476,
    #          600727524, 40042580, 247503992, 913555530, 483175114, 22363795, 805184996, 581234996, 272927971, 584586872, 462362840, 643206446, 54682859, 691867698, 704691074, 1010665647,
    #          426396134, 775579937, 6952392]

    list_u = [
        90817495, 83199265, 229366471, 220404050, 114792533, 266154093, 71703157, 255288531, 179941235, 212929435,
         172539909, 205439092, 22056611, 57538617, 46896897, 71480002, 151682693, 113733933, 224582054, 122573247,
          238781598, 161516207, 269014791, 166131744, 241693844, 124796269, 192963196, 249072244, 220404050, 254127478,
           238350481, 10443671, 185450384, 214427010, 141626475, 220404050, 114792533, 266154093, 71703157, 220404050,
            121823269, 228930541, 42280227, 122052630, 136084294, 63790296, 12220479, 220533477, 97482389, 166164006,
             153363646, 247709004, 241832673, 224600326, 39737394, 230704725, 30262844, 146394438
    ]

    n = 270263047
    e = 3301

    rsa_key = RSA.brute_force(n, e)

    print(RSA.decode_list(list_u, rsa_key))
