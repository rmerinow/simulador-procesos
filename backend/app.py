from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------- DB SIMPLE ----------
def conectar_db():
    conn = sqlite3.connect("simulador.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipos_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

# ---------- RUTAS ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "estado": "ok",
        "mensaje": "Backend Flask funcionando"
    })

@app.route("/crear_equipo_base", methods=["POST"])
def crear_equipo_base():
    data = request.json

    if not data or "nombre" not in data or "tipo" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    conn, cursor = conectar_db()
    cursor.execute(
        "INSERT INTO equipos_base (nombre, tipo) VALUES (?, ?)",
        (data["nombre"], data["tipo"])
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": nuevo_id,
        "mensaje": "Equipo base creado correctamente"
    })

@app.route("/listar_equipos_base", methods=["GET"])
def listar_equipos_base():
    conn, cursor = conectar_db()
    cursor.execute("SELECT id, nombre, tipo FROM equipos_base")
    filas = cursor.fetchall()
    conn.close()

    equipos = []
    for fila in filas:
        equipos.append({
            "id": fila[0],
            "nombre": fila[1],
            "tipo": fila[2]
        })

    return jsonify(equipos)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

