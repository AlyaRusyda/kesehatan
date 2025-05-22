import mysql.connector

def get_conn():
    return mysql.connector.connect(user='root', password='', database='kesehatan')

from datetime import datetime

def buat_janji():
    conn = get_conn()
    cursor = conn.cursor()

    nama_input = input("Masukkan nama dokter: ").strip()

    cursor.execute(
        "SELECT id_dokter, nama_dokter, jadwal_kerja FROM dokter WHERE nama_dokter LIKE %s",
        (f"%{nama_input}%",)
    )
    results = cursor.fetchall()

    if not results:
        print("❌ Tidak ada dokter yang cocok.")
        conn.close()
        return

    if len(results) > 1:
        print("\n🔍 Ditemukan beberapa dokter:")
        for i, (id_dokter, nama_dokter, jadwal) in enumerate(results, 1):
            print(f"{i}. {nama_dokter} | Jadwal: {jadwal}")
        pilihan = input("Pilih nomor dokter: ")
        try:
            pilihan = int(pilihan) - 1
            id_dokter, nama_dokter, jadwal = results[pilihan]
        except:
            print("❌ Pilihan tidak valid.")
            conn.close()
            return
    else:
        id_dokter, nama_dokter, jadwal = results[0]

    print(f"\n🩺 Jadwal kerja {nama_dokter}: {jadwal}")

    try:
        bagian_hari, bagian_jam = jadwal.split(',')
        hari_kerja_str = bagian_hari.lower().strip()
        jam_mulai_str, jam_selesai_str = [j.strip() for j in bagian_jam.strip().split('-')]
        jam_mulai = datetime.strptime(jam_mulai_str, "%H:%M").time()
        jam_selesai = datetime.strptime(jam_selesai_str, "%H:%M").time()
    except:
        print("❌ Format jadwal dokter tidak valid. Harus: Hari, HH:MM - HH:MM")
        conn.close()
        return

    tanggal_input = input("Masukkan tanggal janji (format: YYYY-MM-DD): ").strip()
    waktu_input = input("Masukkan waktu janji (format HH:MM): ").strip()

    try:
        datetime_str = f"{tanggal_input} {waktu_input}:00"
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        waktu_janji = datetime_obj.time()

        hari_indo = {
            "Monday": "senin", "Tuesday": "selasa", "Wednesday": "rabu",
            "Thursday": "kamis", "Friday": "jumat", "Saturday": "sabtu", "Sunday": "minggu"
        }
        hari_dari_tanggal = hari_indo[datetime_obj.strftime("%A")]

        if hari_dari_tanggal not in hari_kerja_str:
            print(f"❌ Dokter tidak praktik pada hari {hari_dari_tanggal.capitalize()}.")
            conn.close()
            return

        if not (jam_mulai <= waktu_janji <= jam_selesai):
            print(f"❌ Waktu janji harus antara {jam_mulai_str} - {jam_selesai_str}.")
            conn.close()
            return

    except ValueError:
        print("❌ Format tanggal atau waktu tidak valid.")
        conn.close()
        return

    id_pasien = input("Masukkan ID pasien: ").strip()

    cursor.execute("""
        SELECT COUNT(*)
        FROM janjitemu
        WHERE id_dokter = %s AND tanggal = %s AND status IN ('menunggu', 'selesai')
    """, (id_dokter, datetime_obj))
    (count_janji,) = cursor.fetchone()
    if count_janji > 0:
        print("❌ Janji temu dengan dokter ini pada tanggal dan jam tersebut sudah ada.")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO janjitemu (tanggal, id_pasien, id_dokter, status) VALUES (%s, %s, %s, %s)",
        (datetime_obj, id_pasien, id_dokter, 'menunggu')
    )
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
    """)
    conn.commit()

    print("✅ Semua janji temu yang lewat dari hari ini dan belum ditindaklanjuti telah dibatalkan otomatis.\n")

    cursor.execute("""
        SELECT id, tanggal, status FROM janjitemu ORDER BY tanggal DESC
    """)
    rows = cursor.fetchall()
    print("📋 Daftar Janji Temu:")
    print("{:<5} {:<20} {:<15}".format("ID", "Tanggal", "Status"))
    print("-" * 45)
    for row in rows:
        print("{:<5} {:<20} {:<15}".format(row[0], row[1].strftime('%Y-%m-%d %H:%M'), row[2]))

    id_janji = input("\nMasukkan ID janji temu yang ingin diubah: ").strip()
    # buat ketika id yang diinput tidak ada maka terdapat warning
    status_baru = input("Masukkan status baru (contoh: 'selesai', 'dibatalkan', dll): ").strip().lower()

    if status_baru == "selesai":
        diagnosa = input("Diagnosa: ")
        resep = input("Resep: ")
        cursor.execute("""
            UPDATE janjitemu
            SET status = %s, diagnosa = %s, resep = %s
            WHERE id = %s
        """, (status_baru, diagnosa, resep, id_janji))
    else:
        cursor.execute("UPDATE janjitemu SET status = %s WHERE id = %s", (status_baru, id_janji))

    conn.commit()
    conn.close()
    print("✅ Status janji temu berhasil diperbarui.")
