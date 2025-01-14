from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

hostname = "5i0t0.h.filess.io"
database = "uas_fireburst"
port = "3305"
username = "uas_fireburst"
password = "fb2528771d31d949d94e7c0f78a392a4306a4176"

def create_connection():
    """ Create a database connection """
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port
        )
        if connection.is_connected():
            print("Connected to MariaDB Server")
            return connection
    except Error as e:
        print("Error while connecting to MariaDB", e)
        return None

@app.route('/')
def halaman_awal():
    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500  # Return an error response

    try:
        cursor = connection.cursor()  # Buat cursor tanpa 'with'
        cursor.execute("SELECT * FROM tbl_konser")
        result = cursor.fetchall()
    except Error as e:
        print("Error fetching data:", e)
        return "Error fetching data from the database.", 500
    finally:
        cursor.close()  # Tutup cursor
        connection.close()  # Tutup koneksi

    return render_template('index.html', hasil=result)

@app.route('/home')
def halaman_home():
    return render_template('home.html')

@app.route('/concert')
def halaman_concert():
    return render_template('concert.html')

@app.route('/contact')
def halaman_contact():
    return render_template('contact.html')

@app.route('/hindia')
def halaman_hindia():
    return render_template('hindia.html')
@app.route('/denny caknan')
def halaman_denny_caknan():
    return render_template('denny caknan.html')
@app.route('/bernadya')
def halaman_bernadya():
    return render_template('bernadya.html')


@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nama_lengkap = request.form['nama_lengkap']
    email = request.form['email']
    nomer_handphone = request.form['nomer_handphone']  # Pastikan ini sesuai
    jumlah_tiket = request.form['jumlah_tiket']
    total_harga = request.form['total_harga']
    nama_konser = request.form['nama_konser']

    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500

    try:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO tbl_konser (nama_lengkap, email, nomer_handphone, jumlah_tiket, total_harga, nama_konser) VALUES (%s, %s, %s, %s, %s, %s)', 
               (nama_lengkap, email, nomer_handphone, jumlah_tiket, total_harga, nama_konser))
            connection.commit()
    except Error as e:
        print("Error inserting data:", e)
        return "Error inserting data into the database.", 500
    finally:
        connection.close()

    return redirect(url_for('halaman_awal'))

if __name__ == '__main__':
    app.run(debug=True)