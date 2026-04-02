array = list(map(int, input("Введите циферки через пробел: ").split()))

sum_odd = 0
for num in array:
    if num % 2 != 0:
        sum_odd += num

print("Сумма нечётных чисел:", sum_odd)