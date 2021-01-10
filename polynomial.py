import numpy as np
import unittest
import random
import itertools


class Poly:
    def __init__(self, coefficients=[]):
        if(len(coefficients) == 0):
            self.coefficients = [0]
        else:
            self.coefficients = np.array(coefficients).astype(np.float32)

    def add(self, other):
        """
        Add two polynomials together. EX : (3x^2 + x - 2) + (3x + 2)
        """
        maxLen = max(len(self.coefficients), len(other.coefficients))
        # pad both array with zeros to have the same length
        sSelf = np.pad(self.coefficients, (0, maxLen - len(self.coefficients)))
        sOther = np.pad(other.coefficients,
                        (0, maxLen - len(other.coefficients)))

        return Poly(np.trim_zeros(np.add(sSelf, sOther), 'b'))

    def subtract(self, other):
        """
        Multiply two polynomials together. EX : (3x^2 + x - 2) - (3x + 2)
        """
        maxLen = max(len(self.coefficients), len(other.coefficients))
        # pad both array with zeros to have the same length
        sSelf = np.pad(self.coefficients, (0, maxLen - len(self.coefficients)))
        sOther = np.pad(other.coefficients,
                        (0, maxLen - len(other.coefficients)))

        return Poly(np.trim_zeros(np.subtract(sSelf, sOther), 'b'))

    def multiply(self, other):
        """
        Multiply two polynomials together. EX : (3x^2 + x - 2) * (3x + 2)
        """
        # create new array with appropriate length for storing result
        newCoefs = [0] * (len(self.coefficients) + len(other.coefficients) - 1)

        for idx, val1 in np.ndenumerate(self.coefficients):
            for jdx, val2 in np.ndenumerate(other.coefficients):
                newCoefs[idx[0] + jdx[0]] += val1 * val2

        return Poly(np.trim_zeros(newCoefs, 'b'))

    def multiply_scalar(self, scalar):
        """
        Multiply a polynomial by a scalar. EX : (3x^2 + x - 2) * 2
        """
        newCoefs = [0] * len(self.coefficients)

        for idx, val in np.ndenumerate(self.coefficients):
            newCoefs[idx[0]] = val * scalar

        return Poly(np.trim_zeros(newCoefs, 'b'))

    def divide(self, divider, includeRemainder=False):
        """
        Divide a polynomial by another polynomial
        """
        maxLen = max(len(self.coefficients), len(divider.coefficients))
        newPoly = Poly([0] * maxLen)
        remainder = Poly(np.copy(self.coefficients))

        dividerDegree = divider.maxDegree()
        remainderDegree = remainder.maxDegree()

        # as long as the degree of the remainder is bigger than the divider continue the division
        while remainderDegree >= dividerDegree:
            # find the division result between the two highest coefficients
            division = remainder.coefficients[remainderDegree] / \
                divider.coefficients[dividerDegree]
            # multiply the divider by the division result and pad it to change it's degree
            toRemove = Poly(np.pad(divider.multiply_scalar(
                division).coefficients, (remainderDegree - dividerDegree, 0)))
            # update result
            newPoly.coefficients[remainderDegree - dividerDegree] = division

            # subtract the divider from the remainder and update it's max degree
            remainder = remainder.subtract(toRemove)
            remainderDegree = remainder.maxDegree()

        newPoly = Poly(np.trim_zeros(newPoly.coefficients, 'b'))
        remainder = Poly(np.trim_zeros(remainder.coefficients, 'b'))

        if(includeRemainder):
            return [newPoly, remainder]
        else:
            return newPoly

    def modulo(self, divider):
        """
        Remainder of the division of a polynomial by another polynomial
        """

        return self.divide(divider, True)[1]

    def maxDegree(self):
        """
        Get the max degree of the poly (3 => x^4 as indexing starts at 0)
        """
        idx = len(self.coefficients) - 1

        while self.coefficients[idx] == 0 and idx >= 0:
            idx -= 1

        return idx

    def eval(self, number):
        """
        Evaluate the polynomial with a certain number
        """
        result = 0

        for i, coef in enumerate(self.coefficients):
            result += coef * pow(number, i)

        return result

    @staticmethod
    def createPointsList(poly, length):
        points = []

        for i in range(0, length):
            points.append(poly.eval(i))

        return points

    @staticmethod
    def insertErrors(pointsList, amount):
        randomIndices = []

        for i in range(0, amount):
            candidate = random.randint(0, len(pointsList)-1)
            if(randomIndices.count(candidate) == 0):
                randomIndices.append(candidate)

        for i in randomIndices:
            pointsList[i] = random.randint(0, 256)

        return pointsList

    @staticmethod
    def formatPointsList(points):
        newList = []

        for i in enumerate(points):
            newList.append(i)

        return newList

    @staticmethod
    def lagrange(points):
        """
        Find the laragange polynomial passing through all the given points.
        """
        amount = len(points)
        upperPolys = [Poly([1])] * amount
        dividers = [1] * amount

        for i, point in enumerate(points):
            for j, other in enumerate(points):
                # skip current number
                if(i == j):
                    continue

                upperPolys[i] *= Poly([-other[0], 1])
                dividers[i] *= point[0] - other[0]

            upperPolys[i] /= Poly([dividers[i]])

        polyResult = Poly()

        for i, poly in enumerate(upperPolys):
            polyResult += Poly([points[i][1]]) * poly

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

        # remove the first + if it exists
        tmp = tmp.strip("+ ")

        return tmp

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __truediv__(self, other):
        return self.divide(other)


class TestingPoly(unittest.TestCase):
    def test_add(self):
        p1 = Poly([0, 2, 3, 1, 1])
        p2 = Poly([4, 10, 3])
        res = p1.add(p2)
        expected = Poly([4, 12, 6, 1, 1])

        print("Addition")
        print(str(res) + ' == ' + str(expected))

        self.assertTrue(np.array_equal(
            res.coefficients, expected.coefficients))

    def test_subtract(self):
        p1 = Poly([0, 2, 3, 1, 1])
        p2 = Poly([4, 10, 3])
        res = p1.subtract(p2)
        expected = Poly([-4, -8, 0, 1, 1])

        print("Substract")
        print(str(res) + ' == ' + str(expected))

        self.assertTrue(np.array_equal(
            res.coefficients, expected.coefficients))

    def test_multiply(self):
        p1 = Poly([0, 5, 2, 10])
        p2 = Poly([5, 3, 1, 12])
        res = p1.multiply(p2)
        expected = Poly([0, 25, 25, 61, 92, 34, 120])

        print("Multiply")
        print(str(res) + ' == ' + str(expected))

        self.assertTrue(np.array_equal(
            res.coefficients, expected.coefficients))

    def test_divide(self):
        p1 = Poly([7, -2, 2, -3])
        p2 = Poly([-2, 1])
        res = p1.divide(p2, True)
        expected = Poly([-10, -4, -3])
        expectedRemainder = Poly([-13])

        print("Divide")
        print(str(res[0]) + ' == ' + str(expected))
        print(str(res[1]) + ' == ' + str(expectedRemainder))

        self.assertTrue(np.array_equal(
            res[0].coefficients, expected.coefficients))
        self.assertTrue(np.array_equal(
            res[1].coefficients, expectedRemainder.coefficients))

    def test_eval(self):
        p = Poly([10, -2, 5])
        res = p.eval(5)
        expected = 125

        self.assertTrue(res == expected)

    def test_lagrange(self):
        points = [[0, 1], [1, 2], [2, 4]]
        lagrangePoly = Poly.lagrange(points)
        expected = Poly([1, 0.5, 0.5])

        print("Lagrange")
        print(str(lagrangePoly) + ' == ' + str(expected))

        self.assertTrue(np.array_equal(
            lagrangePoly.coefficients, expected.coefficients))


if __name__ == '__main__':
    # unittest.main()

    p1 = Poly([5, 2, 45, 3,5])

    points = Poly.createPointsList(p1, 7)
    print(f"Original list : {points}")
    points = Poly.insertErrors(points, 1)
    print(f"Altered list : {points}")

    formatList = Poly.formatPointsList(points)

    polyLagrange = []
    for i in itertools.combinations(formatList, len(p1.coefficients)):
        candidate = Poly.lagrange(i)

        if(polyLagrange.count(candidate) == 0):
            polyLagrange.append(candidate)

    for i in polyLagrange:
        print(i)
