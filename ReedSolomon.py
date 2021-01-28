import random
import copy
from polynomial import Poly
import itertools


class RS:
    @staticmethod
    def createPointsList(poly, length):
        """
        Creates a list of points by evaluating a polynomial from 0 to length.
        """
        points = []

        for i in range(0, length):
            points.append(poly.eval(i))

        return points

    @staticmethod
    def insertErrors(pointsList, amount, mod, beforeIndex=-1):
        """
        Inserts an amount of errors from 0 to mod before the given index.

        ex: pointsList([0, 1, 2, 3, 4, 5])  amount(2) mod(6) beforeIndex(3)
        returns: [5, 2, 2, 3, 4, 5]
        """
        newList = copy.deepcopy(pointsList)
        randomIndices = []

        # by default take the last index of the given list
        if(beforeIndex == -1):
            beforeIndex = len(pointsList) - 1
        elif(beforeIndex < amount):
            raise Exception("beforeIndex cannot be less than amount")

        # get a list {amount} of random distinct indices
        while len(randomIndices) < amount:
            candidate = random.randint(0, beforeIndex)
            if(randomIndices.count(candidate) == 0):
                randomIndices.append(candidate)

        for i in randomIndices:
            newList[i] = random.randint(0, mod)

        return newList

    @staticmethod
    def formatListWithIndices(pointsList):
        """
        Insert indices in a list of numbers.

        list: {10, 14, 16}
        returns: {[0,10], [1,14], [2,16]}
        """
        newList = [0] * len(pointsList)

        for i in range(0, len(pointsList)):
            newList[i] = [i, pointsList[i]]

        return tuple(newList)

    @staticmethod
    def skewedCombinations(pointsList, size, validAfterIndex):
        """
        Get all the combinations of a given size in a given list with fixed validated indices.

        ex : list(25) size(10) validAfterIndex(20)

              --alterable--  -----fixed----\n
        it0: {0, 1, 2, 3, 4, 20,21,22,23,24}\n
        it1: {0, 1, 2, 3, 5, 20,21,22,23,24}\n
        it2: {0, 1, 2, 3, 6, 20,21,22,23,24}\n
        ...
        """
        indices = list(range(size))  # initialise list (0, 1, 2, ... > size)
        # errors are situated before index of original array
        errorBefore = validAfterIndex
        # invalid indices are before this index
        invalidBefore = size - (len(pointsList) - validAfterIndex)

        # fix all the known valid indices
        for i in range(validAfterIndex, len(pointsList), 1):
            relativeI = i - validAfterIndex + invalidBefore
            indices[relativeI] = i

        # return all combinations for the indices where the error could be situated
        for i in itertools.combinations(range(errorBefore), invalidBefore):
            # modify the indices where the error could be
            for idx, val in enumerate(i):
                indices[idx] = val

            # return the selected indices combination, and return an array of : (id, value)
            values = [0] * size
            for idx, valueIdx in enumerate(indices):
                values[idx] = [valueIdx, pointsList[valueIdx]]

            yield values

if __name__ == '__main__':
    points = [83, 111, 114, 125, 101, 122, 63, 109, 111, 132, 62, 133, 137, 32, 150, 224, 80, 98, 165, 110, 32, 115, 97, 110, 103, 107, 88, 211, 112, 68, 168, 180, 35, 24, 29, 204, 117, 120, 98, 116, 110, 3, 131]

    primeNumber = 257
    originalLength = 25
    addedPoints = len(points) - originalLength
    validAfterIndex = 20

    # in all skewed combinations
    for i in RS.skewedCombinations(points, originalLength, validAfterIndex):
        # get the lagrange polynomial going throught the current combination
        candidate = Poly.lagrange(i, primeNumber)

        #count by how many polynomials
        count = 0
        for idx, val in enumerate(points):
            if(candidate.eval(idx) == val):
                count += 1
        #
        if(count >= (originalLength + addedPoints / 2)):
            print(f"Found correct polynomial {candidate}")
            recreated_points = RS.createPointsList(candidate, len(points))
            recreated_text = [chr(recreated_points[j]) for j in range(originalLength)]
            print("".join(recreated_text))
            break
