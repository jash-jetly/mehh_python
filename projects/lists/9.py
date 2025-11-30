def ftp(ip, v):
    try:
        return ip.index(v)
    except ValueError:
        return "nahhhhhh"

if __name__ == "__main__":
    m_t = (10, 20, 30, 40, 50)
    vtf = int(input("Enter a number: "))
    i = ftp(m_t, vtf)
    print(f"The index of  in the tuple is: {i}")

