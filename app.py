from flask import Flask, request, redirect, url_for, render_template
import os, sqlite3, hashlib
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def db_connection():
    conn = sqlite3.connect("ged.db")
    return conn

@app.route("/")
def index():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS documentos (id INTEGER PRIMARY KEY, filename TEXT, hash TEXT, status TEXT, criado_em TEXT)")
    cur.execute("SELECT id, filename, status, criado_em FROM documentos")
    docs = cur.fetchall()
    conn.close()
    return render_template("index.html", docs=docs)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        hash_file = hashlib.sha256(open(path,"rb").read()).hexdigest()
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO documentos (filename, hash, status, criado_em) VALUES (?,?,?,?)",
                    (file.filename, hash_file, "pendente", datetime.now()))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
