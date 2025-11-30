def r_d(i_l):
  n_l = []
  for i in i_l:
    if i not in n_l:
      n_l.append(i)
  return n_l

if __name__ == "__main__":
  m_l = [1, 2, 2, 3, 4, 4, 5]
  u_l = r_d(m_l)
  print(u_l)

