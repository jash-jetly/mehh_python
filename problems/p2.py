def is_leap_year(year):
  """
  Checks if a given year is a leap year.

  Args:
    year: The year to check (an integer).

  Returns:
    True if the year is a leap year, False otherwise.
  """
  if year % 4 == 0:
    if year % 100 == 0:
      if year % 400 == 0:
        return True
      else:
        return False
    else:
      return True
  else:
    return False

if __name__ == '__main__':
  year = int(input("Enter a year: "))
  if is_leap_year(year):
    print(f"{year} is a leap year.")
  else:
    print(f"{year} is not a leap year.")

