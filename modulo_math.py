import numpy as np
import unittest
import math


class ModuloMath:
    @staticmethod
    def powers_of_2(number):
        """
        Returns an array of the powers of 2's that a number is composed of.\n
        Ex: number=67 : result=[0,1,6] (1+2+64)
        """
        i = 0
        result = []
        rest = number

        while(rest > 0):
            if(rest % 2 != 0):
                result.append(i)

            rest = rest // 2
            i += 1

        return result

    @staticmethod
    def rapid_exponentiation(number, exponent, modulus):
        """
        Returns the result of : a^e mod x, by using the rapid exponentiation algorithm.
        """
        # array to store the result of each power of 2
        # number = 8, exponent = 67, modulus = 13
        # i=0 : 8^1 mod 13 = 8
        # i=1 : 8^2 mod 13 = 12
        # i=2 : 8^4 mod 13 = 12^2 mod 13 = 1
        results = [0] * int(math.floor(math.log(exponent, 2)) + 1)
        results[0] = number % modulus

        # compute modulo results for every power of 2
        for i in range(1, len(results)):
            results[i] = pow(results[i-1], 2) % modulus

        # compute the product of every power of 2 present in the original exponent
        result = 1
        for i in ModuloMath.powers_of_2(exponent):
            result *= results[i]

        return result % modulus

    @staticmethod
    def euclid_extended(a, b):
        """
        Returns the GCD of a and b and the coefficients of Bézout's identity as GCD(a,b) = a*x + b*y\n
        /!\\ a >= b
        """
        # setup queues to only store the necessary calculations
        r = [a, b]
        x = [1, 0]
        y = [0, 1]

        while r[1] != 0:
            q = r[0] // r[1]
            # compute the next values of r, x and y
            r.append(r[0] % r[1])
            x.append(x[0] - q * x[1])
            y.append(y[0] - q * y[1])

            # remove from queue the firsts calculations since they arent needed anymore
            r.pop(0)
            x.pop(0)
            y.pop(0)

            # print(f"q = {q}, ri = {r[1]}, xi = {x[1]}, yi = {y[1]}")

        return (r[0], x[0], y[0])

    @staticmethod
    def euler_index(number):
        """
        Returns euler's index for a given number\n
        Ex: number=14 : result=6
        """
        i = 2
        count = 1

        while i < number:
            if(ModuloMath.euclid_extended(number, i)[0] == 1):
                count += 1
            
            i += 1

        return count


class TestingModuloMath(unittest.TestCase):
    def test_powers_of_2(self):
        number = 67
        result = ModuloMath.powers_of_2(number)

        print("\nPowers of 2")
        print(f"{number} == {result}")

        self.assertTrue(np.array_equal([0, 1, 6], result))

    def test_rapid_exponentiation(self):
        number = 8
        exponent = 67
        modulus = 13
        result = ModuloMath.rapid_exponentiation(number, exponent, modulus)

        print("\nRapid exponentiation")
        print(f"{number}^{exponent} mod {modulus} == {result}")

        self.assertEqual(result, 5)

        number = 4
        exponent = 13
        modulus = 497
        result = ModuloMath.rapid_exponentiation(number, exponent, modulus)

        print(f"{number}^{exponent} mod {modulus} == {result}")

        self.assertEqual(result, 445)
        number = 60
        exponent = 53
        modulus = 21
        result = ModuloMath.rapid_exponentiation(number, exponent, modulus)

        print(f"{number}^{exponent} mod {modulus} == {result}")

        self.assertEqual(result, 9)

    def test_euclid_extended(self):
        a = 720
        b = 504
        result = ModuloMath.euclid_extended(a, b)

        print("\nEuclid extended")
        print(
            f"GCD({a}, {b}) == {result[0]} == {a}*{result[1]} + {b}*{result[2]}")

        self.assertTrue(np.array_equal([72, -2, 3], result))

        a = 240
        b = 46
        result = ModuloMath.euclid_extended(a, b)

        print(
            f"GCD({a}, {b}) == {result[0]} == {a}*{result[1]} + {b}*{result[2]}")

        self.assertTrue(np.array_equal([2, -9, 47], result))

    def test_euler_index(self):
        number = 14
        result = ModuloMath.euler_index(number)

        print("\nEuler index")
        print(f"{number} -> {result}")

        self.assertEqual(6, result)

        number = 17
        result = ModuloMath.euler_index(number)

        print(f"{number} -> {result}")

        self.assertEqual(16, result)

if __name__ == '__main__':
    unittest.main()
