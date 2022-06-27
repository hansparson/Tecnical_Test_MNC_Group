
harga_barang = int(input('Masukkan Harga Barang : '))
uang_dibayarkan = int(input('Jumlah uang Dibayarkan : '))

kembalian = uang_dibayarkan - harga_barang
kembalian = round(kembalian-50, -2)

coin = [100000,50000,20000,10000,5000,2000,500,200,100]

if uang_dibayarkan - harga_barang > 0:
    print("Kembalian Uang = " + str(kembalian))
    for c in coin:
        count = 0
        while kembalian>=c:
            kembalian = kembalian-c
            count = count + 1
        if(count != 0):
            if(c == 500 or c == 200 or c ==100):
                print(str(count) + " Koin uang " + str(c))
            else:
                print(str(count) + " Lembar Uang " + str(c))

else:
    print("False, Kurang Bayar")
    
        