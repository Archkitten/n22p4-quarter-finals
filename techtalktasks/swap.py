def swap1(a, b):
    if a > b:
        b, a = a, b
    return a, b


def swap1_helper(a, b):
    print("python swap")
    print("original: ", a, b)
    a, b = swap1(a, b)
    print("after: ", a, b)
    print()


def swap2(a, b):
    if a > b:
        swap = a
        a = b
        b = swap
    return a, b


def swap2_helper(a, b):
    print("classic swap")
    print("original ", a, b)
    a, b = swap2(a, b)
    print("after: ", a, b)
    print()


def test_swappers():
    swap1_helper(12, 10)
    swap1_helper(32, 38)
    swap1_helper(51, 23)
    swap2_helper(12, 10)
    swap2_helper(32, 38)
    swap2_helper(51, 23)


if __name__ == "__main__":
    test_swappers()
