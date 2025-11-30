def lnt(i_l):
  m_t = tuple(i_l)
  m_l = list(m_t)
  return m_t, m_l

if __name__ == '__main__':
  m_l = [1, 2, 3, 4, 5, 5]
  m_t, mla = lnt(m_l)

  print("Original list:", m_l)
  print("Tuple:", m_t)
  print("List again:", mla)

