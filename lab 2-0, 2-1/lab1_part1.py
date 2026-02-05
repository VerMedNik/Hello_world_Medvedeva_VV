print ("Hello world")
print ("Surname: Medvedeva, Name: Veronika, Group 4731901/5002, yaer: 2025")
print (5, 2, 2026, sep=".")
print ("Предмет\t Оценка\n Математика\t 5\n Физика    \t 4\n Информатика\t 5")
name = "Veronika"
n = "4731901/5002"
xp = "10560" 
print (f"Student {name} from group {n} recieve {xp} points")
f = open("out.txt", "w", encoding="utf-8")
print("About me", file = f)
f.close()