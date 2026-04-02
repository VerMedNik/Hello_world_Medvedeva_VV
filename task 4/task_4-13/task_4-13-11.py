array = list(map(int, input("Введите циферки через пробел: ").split()))

sum_odd_index = 0
for i in range(len(array)):
    if i % 2 == 0:
        sum_odd_index += array[i]

average = sum_odd_index / len(array)

print("Среднее арифметическое:", average)