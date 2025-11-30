def calculate(num1, num2):


    sr = num1 + num2
    dr = num1 - num2
    pr = num1 * num2

    print("Sum:", sr)
    print("Difference:", dr)
    print("Product:", pr)

if __name__ == "__main__":
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))
    calculate(num1, num2)

