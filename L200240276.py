import L200240220, L200240223, L200240290, L200240267

def main():
    # looping print selama program dijalankan
    while True:
        print('''
Program Manajemen Rumah Sakit
Welcome Admin

Pilih aksi:
1. Administrasi Pasien
2. Administrasi Dokter
3. Buat Janji Temu
4. Laporan Janji Temu
5. Janji Temu Dokter
6. Ubah Status Janji Temu
0. Keluar
''')

        # mengambil input user
        action = input("Masukkan pilihan aksi: ")

        # mengarahkan ke fungsi berdasarkan input user
        if action == '1':
            menu_pasien()
        elif action == '2':
            menu_dokter()
        elif action == '3':
            L200240290.buat_janji()
        elif action == '4':
            L200240267.join()
        elif action == '5':
            L200240267.agregat()
        elif action == '6':
            L200240290.ubah_status()
        elif action == '0':
            print("Terima kasih.")
            break
        else:
            print("Pilihan tidak tersedia")

def menu_pasien():
    while True:
        print('''
Manajemen Pasien:
1. Lihat Daftar Pasien
2. Registrasi Pasien
3. Ubah Nomor Telepon Pasien
4. Hapus Data Pasien
0. Kembali
''')
        aksi = input("Pilih: ") # input aksi yang akan dilakukan
        # mengeksekusi aksi sesuai dengan input user
        if aksi == '1':
            L200240220.lihat()
        elif aksi == '2':
            L200240220.tambah()
        elif aksi == '3':
            L200240220.ubah()
        elif aksi == '4':
            L200240220.hapus()
        elif aksi == '0':
            break
        else:
            print("Pilihan tidak valid.")

def menu_dokter():
    while True:
        print('''
Manajemen Dokter:
1. Daftar Dokter Aktif
2. Tambah Data Dokter
3. Ubah Data Dokter
4. Hapus Data Dokter
0. Kembali
''')
        aksi = input("Pilih: ") # input aksi yang akan dilakukan
        # mengeksekusi aksi sesuai dengan input user
        if aksi == '1':
            L200240223.lihat()
        elif aksi == '2':
            L200240223.tambah()
        elif aksi == '3':
            L200240223.ubah()
        elif aksi == '4':
            L200240223.hapus()
        elif aksi == '0':
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
