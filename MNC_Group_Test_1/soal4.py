from datetime import datetime

cuti_kantor = 14
cuti_bersama = int(input('Jumlah Cuti Bersama : '))
tanggal_join = str(input('Tanggal join karyawan : '))
tanggal_join = datetime.strptime(tanggal_join, '%Y-%m-%d').date()
rencana_cuti = str(input('Tanggal rencana cuti : '))
rencana_cuti = datetime.strptime(rencana_cuti, '%Y-%m-%d').date()
durasi_cuti = int(input('Durasi cuti (hari) : '))


#### Total Cuti Karyawan baru
delta = rencana_cuti - tanggal_join
print(delta.days)
if delta.days < 180:
    print("False")
    print("Alasan: Karena belum 180 hari sejak tanggal join karyawan")
else:
    print("disetujui")
    
###### Total Cuti Disetujui
cuti_pribadi = cuti_kantor - cuti_bersama


################ Bingung Soalnya (｡•́︿•̀｡)(｡•́︿•̀｡)(｡•́︿•̀｡)(｡•́︿•̀｡)(｡•́︿•̀｡)
