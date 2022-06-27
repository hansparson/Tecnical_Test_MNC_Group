array2 = []
# array2 = ["satu", "sate", "tujuh", "tusuk", 'tujuh', "sate", "bonus", "tiga", "puluh", "tujuh", "tusuk"]

n = int(input("Masukkan jumlah Array : "))
  
for i in range(0, n):
    ele = str(input("Input Array {} : ".format(i+1)))
    array2.append(ele) 
      

kata_terdekat = ""
terdekat = n
hasil = ""

for x in range(len(array2)):
    nilai_aktif = array2[x]
    for a in range(x+1, len(array2)):
        if array2[a] == nilai_aktif:
            # print(array2[a] +" "+ str(a)+" "+ str(x))
            nilai = a-x
            if a-x < terdekat:
                kata_terdekat = array2[a]
                terdekat = a - x

# print(kata_terdekat)

for posisi in range(len(array2)):
    if array2[posisi] == kata_terdekat:
        hasil = hasil + str(posisi+1) + " "

print(hasil)
