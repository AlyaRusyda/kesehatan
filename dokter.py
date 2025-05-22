import mysql.connector

def get_conn():
    return mysql.connector.connect(user='root', password='', database='kesehatan')

def lihat():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dokter")
    rows = cursor.fetchall()
    conn.close()

    print("\n=== Daftar Dokter ===")
    print("{:<5} {:<20} {:<25} {:<15} {:<30}".format("ID", "Nama", "Spesialisasi", "Lisensi", "Jadwal Kerja"))
    print("-" * 105)
    for row in rows:
        id_, nama, spesialis, lisensi, jadwal = row
        print("{:<5} {:<20} {:<25} {:<15} {:<30}".format(id_, nama, spesialis, lisensi, jadwal[:27] + '...' if len(jadwal) > 30 else jadwal))

from datetime import datetime

def tambah():
    conn = get_conn()
    cursor = conn.cursor()
    
    nama = input("Nama Dokter: ")
    spesialis = input("Spesialisasi: ")
    lisensi = input("No. Lisensi: ")
    
    print("\n--- Input Jadwal Kerja ---")
    print("Contoh hari: Senin, Selasa, Rabu (gunakan koma atau rentang hari)")
    hari_kerja = input("Hari kerja dokter: ").strip()
    
    try:
        jam_mulai = input("Jam mulai praktik (format HH:MM, contoh 08:00): ").strip()
        jam_selesai = input("Jam selesai praktik (format HH:MM, contoh 15:00): ").strip()

        waktu_mulai = datetime.strptime(jam_mulai, "%H:%M")
        waktu_selesai = datetime.strptime(jam_selesai, "%H:%M")

        if waktu_mulai >= waktu_selesai:
            print("❌ Jam mulai harus lebih awal dari jam selesai.")
            conn.close()
            return

        jadwal = f"{hari_kerja}, {jam_mulai} - {jam_selesai}"

        cursor.execute(
            "INSERT INTO dokter (nama_dokter, spesialisasi, nomor_lisensi, jadwal_kerja) VALUES (%s,%s,%s,%s)",
            (nama, spesialis, lisensi, jadwal)
        )
        conn.commit()
        print("✅ Dokter berhasil ditambahkan dengan jadwal:", jadwal)

    except ValueError:
        print("❌ Format waktu salah. Gunakan format HH:MM, contoh 08:00.")
    
    conn.close()

def ubah():
    conn = get_conn()
    cursor = conn.cursor()
    lihat()
    id_dokter = input('''
Pilih ID dokter yang ingin diubah: ''')
    jadwal = input("Jadwal baru: ")
    cursor.execute("UPDATE dokter SET jadwal_kerja = %s WHERE id_dokter = %s", (jadwal, id_dokter))
    conn.commit()
    conn.close()

def hapus():
    conn = get_conn()
    cursor = conn.cursor()
    lihat()
    id_dok = input('''
Pilih ID dokter yang ingin dihapus: ''')
    cursor.execute("DELETE FROM dokter WHERE id_dokter = %s", (id_dok,))
    conn.commit()
    conn.close()

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
