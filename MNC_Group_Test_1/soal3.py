
import time

nilai_string = str(input('Massukkan String: '))
split_string = list(nilai_string)
total_array = len(split_string)
print(total_array)

kurung_kotak = 0
kurung_kurawal = 0
kurung_sudut = 0
kondisi = True

if (total_array % 2) == 0:
    for x in range(total_array):
        print(split_string[x])
        if split_string[x] == '{':
            kurung_kurawal = kurung_kurawal+100
        if split_string[x] == '[':
            kurung_kotak = kurung_kotak+10
        if split_string[x] == '<':
            kurung_sudut = kurung_sudut+1
        if split_string[x] == '}':
            kurung_kurawal = kurung_kurawal-100
        if split_string[x] == ']':
            kurung_kotak = kurung_kotak-10
        if split_string[x] == '>':
            kurung_sudut = kurung_sudut-1

        if(kurung_kurawal < 0 or kurung_kotak < 0 or kurung_sudut <0): ### Kondisi Diketahui jika ada yang tutup kurung duluan maka akan menghasilakn nilai mines
            kondisi = False
        # print(kurung_kurawal, kurung_kotak, kurung_sudut)
        # time.sleep(2)
    if(kurung_kurawal != 0 or kurung_kotak != 0 or kurung_sudut !=0): #jika tidak mines dan nilai tdk sama dengan nol berarti ada kurung yang kelebihan tanpa penutup
            kondisi = False
    print(kondisi)

else:
    print("False")

