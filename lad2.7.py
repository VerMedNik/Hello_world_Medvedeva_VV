#Задание 1
files = ["seq1","seq2","seq3","seq4"]
for name in files:
    new_name = name + ".fasta" + " 17.02.2026"
    print(f"{new_name}")

#Задание 3
seqq1 = "AAATATGAAGAG"
seqq2 = "CCCGATGATAG"
print(seqq1)
for letter in seqq1:
    print(f"{letter}")
print(seqq2)
for letter in seqq2:
    print(f"{letter}")
print("Цикл выполнен")