def msl(l1, l2):
  m_l = l1 + l2
  m_l.sort()
  return m_l

if __name__ == '__main__':
  l1 = [3, 1, 4, 1, 5, 9, 2, 6]
  l2 = [6, 5, 3, 5]
  mas = msl(l1, l2)
  print(f"MAS: {mas}")

