def addition(x, y):
    return x + y
def subtraction(x, y):
    return x - y
def multiplication(x, y):
    return x * y
def division(x, y):
    if y != 0:
        return x / y
    else:
        return "Error! division by zero"
    
def main():
    print("Welcome to the Simple Calculator!")

    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    while True:
        try:
            choice = input("Enter choice(1/2/3/4): ")

            if choice in ['1', '2', '3', '4']:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if choice == '1':
                    print(f"The result is: {addition(num1, num2)}")
                elif choice == '2':
                    print(f"The result is: {subtraction(num1, num2)}")
                elif choice == '3':
                    print(f"The result is: {multiplication(num1, num2)}")
                elif choice == '4':
                    print(f"The result is: {division(num1, num2)}")
                break 
            else:
                print("Invalid Input. Please enter a number between 1 and 4.")

        except ValueError:
            print("Invalid input. Please enter numeric values only.")

if __name__ == "__main__":
    main()



    


