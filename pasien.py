import mysql.connector

# membuat koneksi baru dengan database
def get_conn():
    return mysql.connector.connect(user='root', password='', database='kesehatan')

def lihat():
    conn = get_conn() # membuat koneksi baru
    cursor = conn.cursor() # membuat kursor
    cursor.execute("SELECT * FROM pasien") # query untuk menampilkan data
    rows = cursor.fetchall() # mengambil semua data dari query
    conn.close() # menutup koneksi

    print("\n=== Daftar Pasien ===")
    print("{:<5} {:<20} {:<30} {:<15} {:<30}".format("ID", "Nama", "Alamat", "No. Telepon", "Riwayat Medis")) # header tabel output
    print("-" * 110)
    for row in rows: # looping untuk menampilkan data
        id_, nama, alamat, telp, riwayat = row
        print("{:<5} {:<20} {:<30} {:<15} {:<30}".format(id_, nama, alamat, telp, riwayat[:27] + '...' if len(riwayat) > 30 else riwayat))

def tambah():
    conn = get_conn() # membuat koneksi baru
    cursor = conn.cursor() # membuat kursor
    nama = input("Nama: ") # input nama pasien
    alamat = input("Alamat: ") # input alamat pasien
    telp = input("No. Telepon: ") # input no. telepon pasien
    riwayat = input("Riwayat Medis: ") # input riwayat medis pasien
    cursor.execute("INSERT INTO pasien (nama_pasien, alamat_pasien, nomor_telepon, riwayat_medis) VALUES (%s,%s,%s,%s)",
                   (nama, alamat, telp, riwayat)) # query untuk menambahkan data sesuai dengan input user
    conn.commit() # mengirim query ke database
    conn.close() # menutup koneksi
    print("Pasien berhasil ditambahkan.")

def ubah():
    conn = get_conn() # membuat koneksi baru
    cursor = conn.cursor() # membuat kursor
    lihat()
    id_pasien = input("ID pasien yang diubah: ") # input ID pasien yang akan diubah
    telp = input("No. Telepon baru: ") # input no. telepon baru pasien
    cursor.execute("UPDATE pasien SET nomor_telepon = %s WHERE id_pasien = %s", (telp, id_pasien)) # query untuk mengubah data sesuai dengan input user
    conn.commit() # mengirim query ke database
    conn.close() # menutup koneksi

def hapus():
    conn = get_conn() # membuat koneksi baru
    cursor = conn.cursor() # membuat kursor
    lihat()
    id_pasien = input("ID pasien yang dihapus: ") # input ID pasien yang akan dihapus
    cursor.execute("DELETE FROM pasien WHERE id_pasien = %s", (id_pasien,)) # query untuk menghapus data sesuai dengan input user
    conn.commit() # mengirim query ke database
    conn.close() # menutup koneksi

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
