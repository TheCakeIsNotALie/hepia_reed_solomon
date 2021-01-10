from polynomial import Poly


def main():
    p1 = Poly([-3, -2, -1, -1, 1])
    p2 = Poly([1, 1,])

    result = p1.divide(p2, True)

    print(result[0])
    print(result[1])

if __name__ == "__main__":
    main()
