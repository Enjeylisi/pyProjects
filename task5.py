n = int(input())

result = []
for i in range(n, 0, -1):
    if i % 2 == 0:
        result.append(str(i))

print(" ".join(result))