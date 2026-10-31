a = float(input())
b = float(input())
action = input()

if action == "+":
    print(a + b)
elif action == "-":
    print(a - b)
elif action == "*":
    print(a * b)
elif action == "/":
    if b == 0:
        print("Ділення на нуль")
    else:
        print(a / b)