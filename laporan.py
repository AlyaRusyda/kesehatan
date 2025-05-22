import mysql.connector

def get_conn():
    return mysql.connector.connect(user='root', password='', database='kesehatan')

def agregat():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.nama_dokter, COUNT(j.id) AS total_janji
        FROM dokter d
        LEFT JOIN janjitemu j ON d.id_dokter = j.id_dokter
        GROUP BY d.id_dokter
    """)
    rows = cursor.fetchall()
    conn.close()

    print("\n=== Jumlah Janji Temu per Dokter ===")
    print("{:<25} {:<10}".format("Nama Dokter", "Jumlah"))
    print("-" * 40)
    for row in rows:
        nama, jumlah = row
        print("{:<25} {:<10}".format(nama, jumlah))

def join():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT j.id, j.tanggal, p.nama_pasien, d.nama_dokter, j.status
        FROM janjitemu j
        JOIN pasien p ON j.id_pasien = p.id_pasien
        JOIN dokter d ON j.id_dokter = d.id_dokter
        ORDER BY j.tanggal DESC
    """)
    results = cursor.fetchall()
    conn.close()

    print("\n=== Laporan Janji Temu ===")
    print("{:<5} {:<20} {:<20} {:<20} {:<10}".format("ID", "Tanggal", "Pasien", "Dokter", "Status"))
    print("-" * 80)
    for row in results:
        id_, tanggal, pasien, dokter, status = row
        print("{:<5} {:<20} {:<20} {:<20} {:<10}".format(
            id_,
            tanggal.strftime('%Y-%m-%d %H:%M'),
            pasien,
            dokter,
            status
        ))
