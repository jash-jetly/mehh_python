def print_greater_than_50(numbers):
  for number in numbers:
    if number > 50:
      print(number)

if __name__ == '__main__':
  numbers = (10, 60, 45, 70, 55, 20, 80)
  print_greater_than_50(numbers)

