import mysql.connector
from datetime import datetime

def get_conn():
    return mysql.connector.connect(user='root', password='', database='kesehatan')

def buat_janji():
    conn = get_conn()
    cursor = conn.cursor()

    nama_input = input("Masukkan nama dokter: ").strip() # meminta input nama dokter kepada user

    cursor.execute(
        "SELECT id_dokter, nama_dokter, jadwal_kerja FROM dokter WHERE nama_dokter LIKE %s",
        (f"%{nama_input}%",)
    ) # query untuk mencari jadwal dokter berdasarkan nama dokter yang diinputkan
    results = cursor.fetchall() 

    if not results: # jika tidak ada dokter yang ditemukan
        print("❌ Tidak ada dokter yang cocok.")
        conn.close()
        return

    if len(results) > 1: # jika ada lebih dari satu dokter yang cocok
        print("\n🔍 Ditemukan beberapa dokter:")
        for i, (id_dokter, nama_dokter, jadwal) in enumerate(results, 1): # menampilkan daftar dokter yang cocok
            print(f"{i}. {nama_dokter} | Jadwal: {jadwal}")
        pilihan = input("Pilih nomor dokter: ") # meminta input nomor dokter yang dipilih oleh user
        try:
            pilihan = int(pilihan) - 1 # mengubah input nomor dokter menjadi index
            id_dokter, nama_dokter, jadwal = results[pilihan]
        except:
            print("❌ Pilihan tidak valid.")
            conn.close()
            return
    else:
        id_dokter, nama_dokter, jadwal = results[0] # mengambil dokter yang cocok saja

    print(f"\n🩺 Jadwal kerja {nama_dokter}: {jadwal}") # menampilkan jadwal dokter yang dipilih

    try:
        bagian_hari, bagian_jam = jadwal.split(',') # memisahkan jadwal menjadi bagian hari dan jam
        hari_kerja_str = bagian_hari.lower().strip() # mengubah hari kerja menjadi string
        jam_mulai_str, jam_selesai_str = [j.strip() for j in bagian_jam.strip().split('-')] # memisahkan jam mulai dan selesai menjadi string
        jam_mulai = datetime.strptime(jam_mulai_str, "%H:%M").time() # mengubah jam mulai menjadi waktu
        jam_selesai = datetime.strptime(jam_selesai_str, "%H:%M").time() # mengubah jam selesai menjadi waktu
    except:
        print("❌ Format jadwal dokter tidak valid. Harus: Hari, HH:MM - HH:MM") # err message
        conn.close()
        return

    tanggal_input = input("Masukkan tanggal janji (format: YYYY-MM-DD): ").strip() # meminta input tanggal janji kepada user
    waktu_input = input("Masukkan waktu janji (format HH:MM): ").strip() # meminta input waktu janji kepada user

    try:
        datetime_str = f"{tanggal_input} {waktu_input}:00" # mengubah tanggal dan waktu janji menjadi string
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S") # mengubah tanggal dan waktu janji menjadi objek datetime
        waktu_janji = datetime_obj.time() # mengubah tanggal dan waktu janji menjadi waktu

        hari_indo = {
            "Monday": "senin", "Tuesday": "selasa", "Wednesday": "rabu",
            "Thursday": "kamis", "Friday": "jumat", "Saturday": "sabtu", "Sunday": "minggu"
        } # dictionary untuk mengubah hari dalam bahasa inggris menjadi bahasa indonesia
        hari_dari_tanggal = hari_indo[datetime_obj.strftime("%A")] # mengubah hari tanggal janji menjadi bahasa indonesia

        if hari_dari_tanggal not in hari_kerja_str: # jika hari tanggal janji tidak termasuk dalam hari kerja dokter
            print(f"❌ Dokter tidak praktik pada hari {hari_dari_tanggal.capitalize()}.")
            conn.close()
            return

        if not (jam_mulai <= waktu_janji <= jam_selesai): # jika waktu janji tidak termasuk dalam jam kerja dokter
            print(f"❌ Waktu janji harus antara {jam_mulai_str} - {jam_selesai_str}.")
            conn.close()
            return

    except ValueError: # jika input tanggal atau waktu janji tidak valid
        print("❌ Format tanggal atau waktu tidak valid.")
        conn.close()
        return

    id_pasien = input("Masukkan ID pasien: ").strip() # meminta input ID pasien kepada user

    cursor.execute("""
        SELECT COUNT(*)
        FROM janjitemu
        WHERE id_dokter = %s AND tanggal = %s AND status IN ('menunggu', 'selesai')
    """, (id_dokter, datetime_obj)) # menghitung jumlah janji temu yang sudah ada pada tanggal yang sama
    (count_janji,) = cursor.fetchone() # mengambil hasil query
    if count_janji > 0: # jika ada janji temu yang sudah ada pada tanggal yang sama
        print("❌ Janji temu dengan dokter ini pada tanggal dan jam tersebut sudah ada.")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO janjitemu (tanggal, id_pasien, id_dokter, status) VALUES (%s, %s, %s, %s)",
        (datetime_obj, id_pasien, id_dokter, 'menunggu')
    ) # menginput janji temu ke dalam database
    conn.commit()
    conn.close()
    print("✅ Janji temu berhasil dibuat.")

def ubah_status():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE janjitemu
        SET status = 'dibatalkan'
        WHERE status = 'menunggu' AND tanggal < NOW()
    """) # mengupdate status janji temu yang sudah melewati tanggal ke 'dibatalkan'
    conn.commit()

    print("✅ Semua janji temu yang lewat dari hari ini dan belum ditindaklanjuti telah dibatalkan otomatis.\n")

    cursor.execute("""
        SELECT id, tanggal, status FROM janjitemu ORDER BY tanggal DESC
    """) # mengambil data janji temu yang sudah ada
    rows = cursor.fetchall() # mengambil hasil query
    print("📋 Daftar Janji Temu:")
    print("{:<5} {:<20} {:<15}".format("ID", "Tanggal", "Status"))
    print("-" * 45)
    for row in rows: # menampilkan data janji temu
        print("{:<5} {:<20} {:<15}".format(row[0], row[1].strftime('%Y-%m-%d %H:%M'), row[2]))

    id_janji = input("\nMasukkan ID janji temu yang ingin diubah: ").strip() # meminta input ID janji temu kepada user
    status_baru = input("Masukkan status baru (contoh: 'selesai', 'dibatalkan', dll): ").strip().lower() # meminta input status baru kepada user

    if status_baru == "selesai": # jika status baru adalah 'selesai'
        diagnosa = input("Diagnosa: ") # meminta input diagnosa kepada user
        resep = input("Resep: ") # meminta input resep kepada user
        cursor.execute("""
            UPDATE janjitemu
            SET status = %s, diagnosa = %s, resep = %s
            WHERE id = %s
        """, (status_baru, diagnosa, resep, id_janji)) # mengupdate status janji temu ke 'selesai' dan menginput diagnosa dan resep
    else:
        cursor.execute("UPDATE janjitemu SET status = %s WHERE id = %s", (status_baru, id_janji)) # mengupdate status janji temu berdasarkan ID yang dimasukkan oleh user

    conn.commit()
    conn.close()
    print("✅ Status janji temu berhasil diperbarui.")
