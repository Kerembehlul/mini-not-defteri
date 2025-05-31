from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )

@app.route('/')
def home():
    return 'Not Defteri API çalışıyor!'

@app.route('/notlar', methods=['GET', 'POST'])
def notlar():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        cur.execute("INSERT INTO notlar (icerik) VALUES (%s)", (data['icerik'],))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mesaj': 'Not eklendi'}), 201

    cur.execute('SELECT * FROM notlar;')
    notlar = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(notlar)
