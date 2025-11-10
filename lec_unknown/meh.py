def check_age(age):
    if age > 18:
        return "sexxx"
    else:
        return "no sexxx"

if __name__ == '__main__':
    age = int(input("Enter your age: "))
    result = check_age(age)
    if result:
        print(result)
    else:
        print("You are not old enough.")

