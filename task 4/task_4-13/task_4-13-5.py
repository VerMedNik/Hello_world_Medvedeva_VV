n = int(input("Сколько цмферек ввам говорят голоса: "))

max_num = None

for i in range(n):
    num = int(input(f"Введите циферки {i + 1}: "))
    
    if max_num is None or num > max_num:
        max_num = num

print("Самая большая циферкаÖ", max_num)