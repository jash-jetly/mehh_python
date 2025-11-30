def c_t(i_l):
    c = {}
    for i in i_l:
        counter = c.get(i, 0)
        c[i] = counter + 1
    return c


if __name__ == "__main__":
    mylist = [1,12,4,14,1,5,6,9,0,1,3,4]
    u_l = c_t(mylist)
    print(u_l)

