def c_to_f(c):
  f = (c * 9/5) + 32
  return f

if __name__ == "__main__":
    c = float(input("Enter temp: "))
    f = c_to_f(c)
    print(f"{f}°F")

