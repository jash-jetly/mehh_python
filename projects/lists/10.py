def mule(lst):
  pr = 1
  for n in lst:
    pr *= n
  return pr

if __name__ == '__main__':
  ml = [1, 2, 3, 4, 5]
  re = mule(ml)
  print(f"product of elements is: {re}")

