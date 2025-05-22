import mysql.connector

def get_conn():
    return mysql.connector.connect(user='root', password='', database='kesehatan')

def lihat():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pasien")
    rows = cursor.fetchall()
    conn.close()

    print("\n=== Daftar Pasien ===")
    print("{:<5} {:<20} {:<30} {:<15} {:<30}".format("ID", "Nama", "Alamat", "No. Telepon", "Riwayat Medis"))
    print("-" * 110)
    for row in rows:
        id_, nama, alamat, telp, riwayat = row
        print("{:<5} {:<20} {:<30} {:<15} {:<30}".format(id_, nama, alamat, telp, riwayat[:27] + '...' if len(riwayat) > 30 else riwayat))

def tambah():
    conn = get_conn()
    cursor = conn.cursor()
    nama = input("Nama: ")
    alamat = input("Alamat: ")
    telp = input("No. Telepon: ")
    riwayat = input("Riwayat Medis: ")
    cursor.execute("INSERT INTO pasien (nama_pasien, alamat_pasien, nomor_telepon, riwayat_medis) VALUES (%s,%s,%s,%s)",
                   (nama, alamat, telp, riwayat))
    conn.commit()
    conn.close()
    print("Pasien berhasil ditambahkan.")

def ubah():
    conn = get_conn()
    cursor = conn.cursor()
    id_pasien = input("ID pasien yang diubah: ")
    telp = input("No. Telepon baru: ")
    cursor.execute("UPDATE pasien SET nomor_telepon = %s WHERE id_pasien = %s", (telp, id_pasien))
    conn.commit()
    conn.close()

def hapus():
    conn = get_conn()
    cursor = conn.cursor()
    id_pasien = input("ID pasien yang dihapus: ")
    cursor.execute("DELETE FROM pasien WHERE id_pasien = %s", (id_pasien,))
    conn.commit()
    conn.close()

def menu_pasien():
    while True:
        print('''
Manajemen Pasien:
1. Lihat Daftar Pasien
2. Registrasi Pasien
3. Ubah Data Pasien
4. Hapus Data Pasien
0. Kembali
''')
        aksi = input("Pilih: ")
        if aksi == '1':
            lihat()
        elif aksi == '2':
            tambah()
        elif aksi == '3':
            ubah()
        elif aksi == '4':
            hapus()
        elif aksi == '0':
            break
        else:
            print("Pilihan tidak valid.")
