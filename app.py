# Import library yang dibutuhkan dari Flask dan modul lainnya
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector  # Untuk koneksi ke database MySQL
import datetime  # Untuk manipulasi tanggal dan waktu
import random  # Untuk fungsi acak (tidak digunakan dalam kode ini)

# Membuat instance Flask
app = Flask(__name__)
app.secret_key = 'secretkey'  # Menentukan secret key untuk flash messages

# Koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",  # Alamat server MySQL, di sini menggunakan localhost
    user="root",  # Username untuk koneksi ke MySQL
    passwd="",  # Password untuk koneksi ke MySQL (kosong untuk pengaturan default)
    database="member_jkt48"  # Nama database yang akan digunakan
)
cursor = db.cursor()  # Membuat cursor untuk menjalankan perintah SQL

# Membuat database jika belum ada
cursor.execute("CREATE DATABASE IF NOT EXISTS member_jkt48")
# Menggunakan database yang sudah dibuat
cursor.execute("USE member_jkt48")

# Membuat tabel pemesanan_tiket jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS pemesanan_tiket (
    id INT AUTO_INCREMENT PRIMARY KEY,  # Kolom id sebagai primary key dengan auto increment
    nama VARCHAR(255),  # Kolom untuk nama pemesan tiket
    umur INT,  # Kolom untuk umur pemesan tiket
    oshi VARCHAR(255),  # Kolom untuk member favorit (oshi)
    jumlah_tiket INT,  # Kolom untuk jumlah tiket yang dipesan
    total_harga INT,  # Kolom untuk total harga tiket yang dipesan
    tanggal_pemesanan DATETIME  # Kolom untuk tanggal pemesanan tiket
)
""")
print("Tabel pemesanan_tiket berhasil dibuat")

# Hapus tabel member jika ada
cursor.execute("DROP TABLE IF EXISTS member")

# Buat tabel member dengan detail
cursor.execute("""
CREATE TABLE IF NOT EXISTS member (
    id INT AUTO_INCREMENT PRIMARY KEY,  # Kolom id sebagai primary key dengan auto increment
    nama VARCHAR(255),  # Kolom untuk nama member
    tahun_bergabung INT,  # Kolom untuk tahun bergabung member
    detail TEXT,  # Kolom untuk detail member
    foto_url VARCHAR(255)  # Kolom untuk URL foto member
)
""")
print("Tabel member berhasil dibuat")

# Daftar member dengan detail dan foto
members_data = [
    ("Marsha", 2021, "Marsha adalah member JKT48 yang bergabung pada tahun 2021.", "marsha.jpg"),
    ("Freya", 2020, "Freya adalah member JKT48 yang bergabung pada tahun 2020.", "freya.jpg"),
    ("Shani", 2014, "Shani adalah member JKT48 yang bergabung pada tahun 2014.", "shani.jpg"),
    ("Gracia", 2019, "Gracia adalah member JKT48 yang bergabung pada tahun 2019.", "gracia.jpg"),
    ("Zee", 2019, "Zee adalah member JKT48 yang bergabung pada tahun 2019.", "zee.jpg"),
    ("Feni", 2019, "Feni adalah member JKT48 yang bergabung pada tahun 2019.", "feni.jpg"),
    ("Gita", 2019, "Gita adalah member JKT48 yang bergabung pada tahun 2019.", "gita.jpg"),
    ("Ella", 2022, "Ella adalah member JKT48 yang bergabung pada tahun 2022.", "ella.jpg"),
    ("Indira", 2022, "Indira adalah member JKT48 yang bergabung pada tahun 2022.", "indira.jpg"),
    ("Michie", 2023, "Michie adalah member JKT48 yang bergabung pada tahun 2023.", "michie.jpg"),
    ("Oline", 2024, "Oline adalah member JKT48 yang bergabung pada tahun 2024.", "oline.jpg"),
    ("Christy", 2024, "Christy adalah member JKT48 yang bergabung pada tahun 2024.", "christy.jpg"),
]

# Mengisi tabel member
cursor.execute("DELETE FROM member")  # Bersihkan tabel member sebelum mengisi data baru
for member in members_data:
    cursor.execute("INSERT INTO member (nama, tahun_bergabung, detail, foto_url) VALUES (%s, %s, %s, %s)", member)
db.commit()  # Menyimpan perubahan ke database

# Membuat kelas untuk member JKT48
class MemberJKT48:
    def __init__(self, nama, tahun_bergabung, detail, foto_url):
        self.nama = nama  # Nama member
        self.tahun_bergabung = tahun_bergabung  # Tahun bergabung member
        self.detail = detail  # Detail member
        self.foto_url = foto_url  # URL foto member

    def info_member(self):
        tahun_sekarang = datetime.datetime.now().year  # Tahun saat ini
        durasi = tahun_sekarang - self.tahun_bergabung  # Durasi member bergabung
        return f"{self.nama} sudah menjadi member JKT48 selama {durasi} tahun. {self.detail}."

# Membuat kelas untuk tiket teater
class TiketTeater:
    harga_per_orang = 200000  # Harga per tiket

    def __init__(self, jumlah_tiket):
        self.jumlah_tiket = jumlah_tiket  # Jumlah tiket yang dipesan

    def total_harga(self):
        return self.jumlah_tiket * TiketTeater.harga_per_orang  # Menghitung total harga

# Membuat kelas untuk perjalanan
class Perjalanan:
    @staticmethod
    def konversi_jam_ke_menit_dan_detik(jam):
        if jam >= 0:
            menit = jam * 60  # Mengkonversi jam ke menit
            detik = jam * 3600  # Mengkonversi jam ke detik
            return menit, detik
        else:
            return None, None

    def __init__(self, jarak_km, kecepatan_km_per_jam):
        self.jarak_km = jarak_km  # Jarak perjalanan dalam km
        self.kecepatan_km_per_jam = kecepatan_km_per_jam  # Kecepatan perjalanan dalam km/jam

    def waktu_perjalanan(self):
        if self.jarak_km > 0 and self.kecepatan_km_per_jam > 0:
            waktu_jam = self.jarak_km / self.kecepatan_km_per_jam  # Menghitung waktu perjalanan dalam jam
            menit, detik = Perjalanan.konversi_jam_ke_menit_dan_detik(waktu_jam)  # Mengkonversi waktu perjalanan ke menit dan detik
            return waktu_jam, menit, detik
        else:
            return None, None, None

# Route untuk halaman utama
@app.route('/')
def index():
    cursor.execute("SELECT nama, tahun_bergabung, detail, foto_url FROM member")
    members = cursor.fetchall()  # Mengambil semua data member dari database
    return render_template('index.html', members=members)  # Render halaman utama dengan data member

# Route untuk mencari member
@app.route('/cari_member', methods=['POST'])
def cari_member():
    nama = request.form['nama_member'].strip()  # Mengambil input nama member dari form
    cursor.execute("SELECT nama, tahun_bergabung, detail, foto_url FROM member WHERE nama = %s", (nama,))
    result = cursor.fetchone()  # Mengambil satu data member berdasarkan nama

    if result:
        member = MemberJKT48(result[0], result[1], result[2], result[3])  # Membuat objek member dengan data yang ditemukan
        flash(member.info_member())  # Menampilkan informasi member dengan flash message
    else:
        flash("Member tidak ditemukan atau input kosong, coba lagi.", 'error')  # Menampilkan pesan error jika member tidak ditemukan

    return redirect(url_for('index'))  # Redirect kembali ke halaman utama

# Route untuk halaman teater
@app.route('/teater')
def teater():
    return render_template('teater.html')  # Render halaman teater

# Route untuk pemesanan tiket
@app.route('/pesan_tiket', methods=['GET', 'POST'])
def pesan_tiket():
    if request.method == 'POST':
        nama = request.form['nama'].strip()  # Mengambil input nama dari form
        umur = int(request.form['umur'].strip())  # Mengambil input umur dari form
        oshi = request.form['oshi']  # Mengambil input oshi dari form
        jumlah_tiket = int(request.form['jumlah_tiket'].strip())  # Mengambil input jumlah tiket dari form
        if nama and umur > 0 and oshi and jumlah_tiket > 0:
            total_harga = jumlah_tiket * TiketTeater.harga_per_orang  # Menghitung total harga tiket
            tanggal_pemesanan = datetime.datetime.now()  # Mengambil tanggal dan waktu pemesanan saat ini
            cursor.execute("INSERT INTO pemesanan_tiket (nama, umur, oshi, jumlah_tiket, total_harga, tanggal_pemesanan) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nama, umur, oshi, jumlah_tiket, total_harga, tanggal_pemesanan))
            db.commit()  # Menyimpan data pemesanan ke database
            flash(f"Pesanan berhasil! atas nama {nama} dengan member kesukaan (oshi) {oshi} dan total tiket yaitu {jumlah_tiket}, Total harga: Rp {total_harga}.")  # Menampilkan pesan sukses
        else:
            flash("Semua data harus diisi dan valid.", 'error')  # Menampilkan pesan error jika data tidak valid
    
    return render_template('pesan_tiket.html', members=[member[0] for member in members_data])  # Render halaman pemesanan tiket dengan daftar member

# Route untuk halaman kontak
@app.route('/kontak')
def kontak():
    return render_template('kontak.html')  # Render halaman kontak

# Route untuk informasi perjalanan
@app.route('/informasi', methods=['GET', 'POST'])
def informasi():
    waktu_perjalanan = None
    menit = None
    detik = None
    if request.method == 'POST':
        jarak = float(request.form['jarak'])  # Mengambil input jarak dari form
        kecepatan = 40  # Kecepatan rata-rata dalam km/jam
        perjalanan = Perjalanan(jarak, kecepatan)  # Membuat objek perjalanan
        waktu_perjalanan, menit, detik = perjalanan.waktu_perjalanan()  # Menghitung waktu perjalanan
        if waktu_perjalanan is not None:
            flash(f"Waktu perjalanan ke teater: {waktu_perjalanan:.2f} jam, {menit:.2f} menit, {detik:.2f} detik.")  # Menampilkan waktu perjalanan dengan flash message

    return render_template('informasi.html', waktu_perjalanan=waktu_perjalanan, menit=menit, detik=detik)  # Render halaman informasi perjalanan

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)  # Menjalankan aplikasi dalam mode debug
