import random

secret_number = random.randint(1, 10)
attempts = 3

for i in range(attempts):
    guess = int(input())
    if guess == secret_number:
        print("Вгадав!")
        break
    elif guess > secret_number:
        print("Менше")
    else:
        print("Більше")