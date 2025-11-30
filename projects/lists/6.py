def sle(lst):
    t = 0
    for n in lst:
        t += n
    return t


if __name__ == "__main__":
    l = [1,2,3,4,5,6,7,8,9,10]
    to=sle(l)
    print(to)

