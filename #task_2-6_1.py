#Задание 2.6
pH = float (input("Введите значение pH:"))

if pH == 7:
    print("Нейтральная среда")
else:
    if pH <7:
        print("Щелочная среда")
    else :
        print("Кислая среда")

#Задание 2.6.2

groop_of_blood_donor = input("Введите фенотип группы крови (0, A, B, AB): ")
groop_of_blood_akcepter = input("Введите фенотип группы крови (0, A, B, AB): ")

if groop_of_blood_akcepter != "0" and groop_of_blood_akcepter !="A" and groop_of_blood_akcepter !="B" and groop_of_blood_akcepter !="AB" and groop_of_blood_donor != "0" and groop_of_blood_donor !="A" and groop_of_blood_donor !="B" and groop_of_blood_donor !="AB":
    print("This is not exist")
else:
    if groop_of_blood_donor == groop_of_blood_akcepter:
        print("you wiil be alive")
    else:
        if groop_of_blood_donor == "0":
            print("you will be alive")
        else:
            if groop_of_blood_donor == "A" and groop_of_blood_akcepter == "AB":
                print("you will be alive")
            else:
                if groop_of_blood_donor == "B" and groop_of_blood_akcepter == "AB":
                    print("you will be alive")
                else:
                    print ("you will be died")

#Задание 2.6.3
path_of_Hero = input("Ты герой, куда пойдешь? Введи куда ты направишься(вверх/вниз/вправо/влево/назад/вперед/диагональ/внутрь себя): ")

if path_of_Hero == "вверх":
    print ("Ты слишком хорошего мнения о себе, ворота закроют перед твоим носом.")
else:
    if path_of_Hero == "вниз":
        print("Ты туда только на два метра отправишься.")
    else:
        if path_of_Hero == "вправо":
            print("Цыгане выкрали коня. Чё же за фигня? Вчера был ещё, а сегодня его нема!")
        else:
            if path_of_Hero == "влево":
                print("Ты смог ограбить банк!Поздравляю!")
            else:
                if path_of_Hero == "назад" :  
                    print("Тебя сожгли в твоей деревне за трусость!")
                else:
                    if path_of_Hero == "вперед":
                        print("Ты врезался в камень и умер от удара тяжелым тупым предметом по голове.")
                        if path_of_Hero == "диагональ":
                            print("Твой конь взбрикнулся и оскарбленно сказал, что он не слон.")
                        else: 
                            if path_of_Hero == "внутрь себя":
                                print("Ты скукожился до размера собственного сердца.")

