import random

print("Trynaa guess a number")
sn = str(random.randint(100, 999))
a = 0
while True:
    g = input("your guess")
    if not g.isdigit() or len(g) != 3:
        print("Invalid input. Please enter a 3-digit number.")
        continue
    a += 1
    if g == sn:
        print(f"you guessed the number in {attempts} attempts.")
        break
    else:
        f = ""
        for i in range(3):
            if g[i] == sn[i]:
                f += "Correct digit and position. "
            elif g[i] in sn:
                f += "Correct digit, wrong position. "
            else:
                f += "Wrong digit. "
            print(f)


