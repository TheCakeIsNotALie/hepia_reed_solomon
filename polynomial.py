import numpy as np
import unittest
import random
from modulo_math import ModuloMath


class helper:
    @staticmethod
    def min(x, y):
        return y ^ ((x ^ y) & -(x < y))

    # Function to find maximum of x and y
    @staticmethod
    def max(x, y):
        return x ^ ((x ^ y) & -(x < y))


class Poly:
    def __init__(self, coefficients=[], mod=2):
        self.mod = mod
        if(len(coefficients) == 0):
            self.coefficients = [0]
        else:
            self.coefficients = [0] * len(coefficients)
            for idx, coef in enumerate(coefficients):
                self.coefficients[idx] = coef % self.mod

    def add(self, other):
        """
        Add two polynomials together. EX : (3x^2 + x - 2) + (3x + 2)
        """
        maxLen = max(len(self.coefficients), len(other.coefficients))
        newArray = [0]*maxLen

        for i in range(maxLen):
            val1 = 0
            val2 = 0
            if(i < len(self.coefficients)):
                val1 = self.coefficients[i]
            if(i < len(other.coefficients)):
                val2 = other.coefficients[i]

            newArray[i] = (val1 + val2) % self.mod

        # trim zeros
        while newArray[-1] == 0 and len(newArray) > 1:
            del newArray[-1]

        return Poly(newArray, self.mod)

    def subtract(self, other):
        """
        Multiply two polynomials together. EX : (3x^2 + x - 2) - (3x + 2)
        """
        maxLen = max(len(self.coefficients), len(other.coefficients))
        newArray = [0]*maxLen

        for i in range(maxLen):
            val1 = 0
            val2 = 0
            if(i < len(self.coefficients)):
                val1 = self.coefficients[i]
            if(i < len(other.coefficients)):
                val2 = other.coefficients[i]

            newArray[i] = (val1 - val2) % self.mod

        while newArray[-1] == 0:
            del newArray[-1]

        return Poly(newArray, self.mod)

    def multiply(self, other):
        """
        Multiply two polynomials together. EX : (3x^2 + x - 2) * (3x + 2)
        """
        # create new array with appropriate length for storing result
        newCoefs = [0] * (len(self.coefficients) + len(other.coefficients) - 1)

        for idx, val1 in np.ndenumerate(self.coefficients):
            for jdx, val2 in np.ndenumerate(other.coefficients):
                newCoefs[idx[0] + jdx[0]] += (val1 * val2) % self.mod

        return Poly(np.trim_zeros(newCoefs, 'b'), self.mod)

    def multiply_scalar(self, scalar):
        """
        Multiply a polynomial by a scalar. EX : (3x^2 + x - 2) * 2
        """
        newCoefs = [0] * len(self.coefficients)

        for idx, val in np.ndenumerate(self.coefficients):
            newCoefs[idx[0]] = (val * scalar) % self.mod

        return Poly(np.trim_zeros(newCoefs, 'b'), self.mod)

    def maxDegree(self):
        """
        Get the max degree of the poly (3 => x^4 as indexing starts at 0)
        """
        idx = len(self.coefficients) - 1

        while self.coefficients[idx] == 0 and idx >= 0:
            idx -= 1

        return idx

    def equals(self, other):
        """
        Deep equals verification between two polynomials.
        """
        return np.array_equal(self.coefficients, other.coefficients) and self.mod == other.mod

    def eval(self, number):
        """
        Evaluate the polynomial with a given number.
        """
        result = self.coefficients[-1]
        for i in range(len(self.coefficients)-1, 0, -1):
            result = (result*number + self.coefficients[i-1]) % self.mod

        return result

    @staticmethod
    def lagrange(points, mod=1):
        """
        Find the laragange polynomial passing through all the given points.
        """
        amount = len(points)
        upperPolys = [Poly([1], mod)] * amount
        dividers = [1] * amount

        for i, point in enumerate(points):
            for j, other in enumerate(points):
                # skip current number
                if(i == j):
                    continue
                # compute the current part of the upper polynomial
                upperPolys[i] *= Poly([-other[0], 1], mod)
                # compute the current part of the divider

                dividers[i] = dividers[i] * ModuloMath.euclid_extended(
                    (point[0] - other[0]), mod)[1] % mod
            # in modular arithmetics, instead of dividing we multiply by the modular inverse found with the extended Euclid algorithm
            upperPolys[i] = upperPolys[i].multiply_scalar(dividers[i])

        polyResult = Poly([], mod)

        for i, poly in enumerate(upperPolys):
            polyResult += Poly([points[i][1]], mod) * poly

        return polyResult

    def __str__(self):
        tmp = ''
        i = len(self.coefficients) - 1

        # write the polynomial in reverse order : 3x^3 +2x^2 -2
        for val in self.coefficients[::-1]:
            if val != 0:
                # write sign (+ or -)
                tmp += '+' if val >= 0 else ''
                # write either number or coefficient and degree
                if i == 0:
                    tmp += '%g' % (val)
                else:
                    tmp += '%g' % (val) + 'x^' + str(i) + ' '
            i -= 1

        tmp += " % " + str(self.mod)

        # remove the first + if it exists
        tmp = tmp.strip("+ ")

        return tmp

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        return self.multiply(other)


class TestingPoly(unittest.TestCase):
    def test_add(self):
        p1 = Poly([0, 2, 3, 1, 1], 11)
        p2 = Poly([4, 10, 3], 11)
        res = p1.add(p2)
        expected = Poly([4, 1, 6, 1, 1], 11)

        print("Addition")
        print(str(res) + ' == ' + str(expected))

        self.assertTrue(res.equals(expected))

    def test_subtract(self):
        p1 = Poly([0, 2, 3, 1, 1], 11)
        p2 = Poly([4, 10, 3], 11)
        res = p1.subtract(p2)
        expected = Poly([7, 3, 0, 1, 1], 11)

        print("Substract")
        print(str(res) + ' == ' + str(expected))

        self.assertTrue(res.equals(expected))

    def test_multiply(self):
        p1 = Poly([0, 5, 2, 10], 13)
        p2 = Poly([5, 3, 1, 12], 13)
        res = p1.multiply(p2)
        expected = Poly([0, 12, 12, 9, 1, 8, 3], 13)

        print("Multiply")
        print(str(res) + ' == ' + str(expected))

        self.assertTrue(res.equals(expected))

    def test_eval(self):
        p = Poly([10, -2, 5], 11)
        res = p.eval(5)
        expected = 4

        self.assertTrue(res == expected)

    def test_lagrange(self):
        p1 = Poly([5, 2, 10, 2, 22], 23)

        points = []

        for i in range(len(p1.coefficients)):
            points.append([i, p1.eval(i)])

        lagrangePoly = Poly.lagrange(points, p1.mod)

        print("Lagrange")
        print(str(lagrangePoly) + ' == ' + str(p1))

        self.assertTrue(lagrangePoly.equals(p1))


if __name__ == '__main__':
    unittest.main()
