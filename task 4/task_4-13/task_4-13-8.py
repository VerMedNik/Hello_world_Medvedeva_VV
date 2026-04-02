array = list(map(int, input("Введите циферки через пробел: ").split()))

count_positive = 0
for num in array:
    if num > 0:
        count_positive += 1

print("Количество положительных циферек:", count_positive)