from flask import Flask, render_template, request, redirect, url_for, abort
import mysql.connector
from mysql.connector import Error
import os
import logging

app = Flask(__name__)

# Load database credentials from environment variables for security
hostname = os.getenv("DB_HOSTNAME", "5i0t0.h.filess.io")
database = os.getenv("DB_DATABASE", "uas_fireburst")
port = os.getenv("DB_PORT", "3305")
username = os.getenv("DB_USERNAME", "uas_fireburst")
password = os.getenv("DB_PASSWORD", "fb2528771d31d949d94e7c0f78a392a4306a4176")

# Configure logging
logging.basicConfig(level=logging.ERROR)

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
        logging.error("Error while connecting to MariaDB: %s", e)
        return None

@app.route('/')
def halaman_awal():
    connection = create_connection()
    if connection is None:
        abort(500, description="Unable to connect to the database.")

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tbl_konser")
        result = cursor.fetchall()
    except Error as e:
        logging.error("Error fetching data: %s", e)
        abort(500, description="Error fetching data from the database.")
    finally:
        cursor.close()
        connection.close()

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

@app.route('/denny_caknan')
def halaman_denny_caknan():
    return render_template('denny caknan.html')

@app.route('/bernadya')
def halaman_bernadya():
    return render_template('bernadya.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nama_lengkap = request.form['nama_lengkap']
    email = request.form['email']
    nomer_handphone = request.form['nomer_handphone']
    jumlah_tiket = request.form['jumlah_tiket']
    total_harga = request.form['total_harga']
    nama_konser = request.form['nama_konser']

    connection = create_connection()
    if connection is None:
        abort(500, description="Unable to connect to the database.")

    try:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO tbl_konser (nama_lengkap, email, nomer_handphone, jumlah_tiket, total_harga, nama_konser) VALUES (%s, %s, %s, %s, %s, %s)', 
                           (nama_lengkap, email, nomer_handphone, jumlah_tiket, total_harga, nama_konser))
            connection.commit()
    except Error as e:
        logging.error("Error inserting data: %s", e)
        abort(500, description="Error inserting data into the database.")
    finally:
        connection.close()

    return redirect(url_for('halaman_home'))

if __name__ == '__main__':
    app.run(debug=True)