def is_palindrome(s):
  s = s.lower()
  return s == s[::-1]

if __name__ == '__main__':
  test_strings = "racecar"
  print(f" {test_strings} is a palindrome: {is_palindrome(test_strings)}")

