import mysql.connector
from datetime import datetime

def get_conn():
    return mysql.connector.connect(user='root', password='', database='kesehatan')

def lihat():
    conn = get_conn() # ambil koneksi
    cursor = conn.cursor() # membuat kursor
    cursor.execute("SELECT * FROM dokter") # query untuk mengambil seluruh kolom dari tabel dokter
    rows = cursor.fetchall() # mengambil semua baris dari hasil query
    conn.close() # menutup koneksi

    print("\n=== Daftar Dokter ===")
    print("{:<5} {:<20} {:<25} {:<15} {:<30}".format("ID", "Nama", "Spesialisasi", "Lisensi", "Jadwal Kerja"))
    print("-" * 105)
    for row in rows: # menampilkan setiap baris hasil query
        id_, nama, spesialis, lisensi, jadwal = row
        print("{:<5} {:<20} {:<25} {:<15} {:<30}".format(id_, nama, spesialis, lisensi, jadwal[:27] + '...' if len(jadwal) > 30 else jadwal))

def tambah():
    conn = get_conn() # ambil koneksi
    cursor = conn.cursor() # membuat kursor
    
    nama = input("Nama Dokter: ") # input nama dokter
    spesialis = input("Spesialisasi: ") # input spesialisasi dokter
    lisensi = input("No. Lisensi: ") # input no. lisensi dokter
    
    print("\n--- Input Jadwal Kerja ---")
    print("Contoh hari: Senin, Selasa, Rabu (gunakan koma atau rentang hari)")
    hari_kerja = input("Hari kerja dokter: ").strip() # input hari kerja dokter
    
    try:
        jam_mulai = input("Jam mulai praktik (format HH:MM, contoh 08:00): ").strip() # input jam mulai praktik
        jam_selesai = input("Jam selesai praktik (format HH:MM, contoh 15:00): ").strip() # input jam selesai praktik

        waktu_mulai = datetime.strptime(jam_mulai, "%H:%M") # konversi jam mulai ke format waktu
        waktu_selesai = datetime.strptime(jam_selesai, "%H:%M") # konversi jam selesai ke format waktu

        if waktu_mulai >= waktu_selesai: # validasi jam praktik
            print("❌ Jam mulai harus lebih awal dari jam selesai.")
            conn.close()
            return

        jadwal = f"{hari_kerja}, {jam_mulai} - {jam_selesai}" # format jadwal kerja

        cursor.execute(
            "INSERT INTO dokter (nama_dokter, spesialisasi, nomor_lisensi, jadwal_kerja) VALUES (%s,%s,%s,%s)",
            (nama, spesialis, lisensi, jadwal)
        ) # query untuk menambahkan dokter baru ke tabel dokter
        conn.commit()
        print("✅ Dokter berhasil ditambahkan dengan jadwal:", jadwal)

    except ValueError: # err handling format waktu
        print("❌ Format waktu salah. Gunakan format HH:MM, contoh 08:00.")
    
    conn.close()

def ubah():
    conn = get_conn() # ambil koneksi
    cursor = conn.cursor() # membuat kursor
    lihat()
    id_dokter = input("\nPilih ID dokter yang ingin diubah: ") # input ID dokter yang ingin diubah
    jadwal = input("Jadwal baru: ") # input jadwal baru
    cursor.execute("UPDATE dokter SET jadwal_kerja = %s WHERE id_dokter = %s", (jadwal, id_dokter)) # query untuk mengubah jadwal dokter
    conn.commit() # commit perubahan
    conn.close() # tutup koneksi

def hapus():
    conn = get_conn() # ambil koneksi
    cursor = conn.cursor() # membuat kursor
    lihat()
    id_dok = input("\nPilih ID dokter yang ingin dihapus: ") # input ID dokter yang ingin dihapus
    cursor.execute("DELETE FROM dokter WHERE id_dokter = %s", (id_dok,)) # query untuk menghapus dokter
    conn.commit() # commit perubahan
    conn.close() # tutup koneksi

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
