# Задание на «РЕФАКТОРИНГ»
name = input("Your name:")

age = input("Your ages:")

print(f"Hello student {name} your ages ", age, " correct ", sep="-", end="?\n")

# Задание на «ГИГИЕНА ВЫВОДА»
python_version = "3.10"

print(f"Language: Python\n\tVersion:{python_version}")

# Задание 2.2(1)
name_cours ="52"
number_of_step ="45"
number_of_complect_exercise = "75"

print(f"Name cours {name_cours} number of step {number_of_step} number of complects exercise {number_of_complect_exercise}")

# Задание 2.2(2)
user_input = input("Somthing ")
processed_input = user_input.upper()

print(f"You tolb {user_input}",f"I heard {processed_input}", sep="->")

# Задание 2.2(3)
name_of_item = "Shtyka"
number_of_item = "049/035/69"
broken_or_you_are_lucky = "you are not lucky - broken"
quantity = "-525"

print(f"You need\t {name_of_item}\n Number\t{number_of_item}\n Broken\t{broken_or_you_are_lucky}\n Qualitity\t{quantity}")

# Задание 2.2(Итоговое задание)
name_of_reactive = input("Name of reactive ")
quantity_of_reactive = input("How much?")

print(f"Реактив {name_of_reactive} поступил на склад в количестве {quantity_of_reactive} шт.")

# Задание 2.3.1
name_of_food_vibe = input("Название питательной среды: ")
qualitu = input("Введите концетрацию: ")
temperatura = input("Введите температуру стерилизации (в цельсиях): ")

with open("recipe.txt","w", encoding = "utf-8") as card:

    card.write(f"{name_of_food_vibe}\n{qualitu}\n{temperatura}")

print("Файл 'recipe.txt' успешно сформирован!")

# Задание 2.3.2
name_of_operator = input("Введите имя оператора: ")
mean_of_sensor = input("Значение давления: ")

with open("sensor_log.txt","w", encoding = "utf-8") as card:

    card.write(f"Имя оператора:\t{name_of_operator}\n Текущее значение давления (Па):{mean_of_sensor}")

print("Данные успешно сохранены в sensor_log.txt")

# Задание 2.3(Итоговое задание)
name_of_screcting = ("ФИО исследователя: ")
data = ("Data: ")
name_of_experement = ("Название эксперимента: ")
itog = ("Вывод: ")

with open("journal.txt","w", encoding = "utf-8") as card:

    card.write(f"\t***\n+\tЭлектронный лабораторный журнал\t+\n ФИО исследователя:\t{name_of_screcting}\n Data:\t{data}\n Эксперимент:\t{name_of_experement}\n Вывод:\t{itog}")

# Задание 2.4.1
massa_belkov = input("Массa белков в продукте (г): ")
massa_girov = input("Массa жиров в продукте (г): ")
massa_uglevodov = input("Массf углеводов в продукте (г): ")
result = massa_belkov*4 + massa_girov*9 + massa_uglevodov*4

print(f"Итого калорийность: {result}")

# Задание 2.4.2
weight_of_body = input("Введите ваш вес (кг): ")
height_of_body = input("Введите ваш рост (м): ")
bmi = weight_of_body / (height_of_body ** 2)

print(f"Рост:\t{height_of_body}\nВес: \t{weight_of_body}\nИндекс массы тела:\t{bmi}")

# Задание 2.4.3
quantity_of_capsul = input("Введите общее количество произведенных капсул: ")
vacum_of_capsul = input("Введите количество капсул в одной упаковке: ")
full_capsils = quantity_of_capsul // vacum_of_capsul
not_full_capsils = quantity_of_capsul % vacum_of_capsul

print(f"Полных упаковок:\t{full_capsils}\nОстаток капсул: \t{not_full_capsils}")

# Задание 2.4(Итоговое задание)
obime_of_NaCl = input("Запросить нужный объем раствора (в мл): ")
massa_of_NaCl = round(mass,2) obime_of_NaCl * 0.009
obime_of_water = obime_of_NaCl

print(f"Общий объем:\t{obime_of_NaCl}\nМасса соли: \t{massa_of_NaCl}\nОбъем воды: {obime_of_water}")

# Задание 2.5 - Выполнено отдельно