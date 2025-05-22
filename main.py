import pasien, dokter, janjitemu, laporan

def main():
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

        action = input("Masukkan pilihan aksi: ")

        if action == '1':
            pasien.menu_pasien()
        elif action == '2':
            dokter.menu_dokter()
        elif action == '3':
            janjitemu.buat_janji()
        elif action == '4':
            laporan.join()
        elif action == '5':
            laporan.agregat()
        elif action == '6':
            janjitemu.ubah_status()
        elif action == '0':
            print("Terima kasih.")
            break
        else:
            print("Pilihan tidak tersedia")

if __name__ == "__main__":
    main()
