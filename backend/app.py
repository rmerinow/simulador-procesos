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
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_id INTEGER NOT NULL,
            tag TEXT NOT NULL,
            FOREIGN KEY (base_id) REFERENCES equipos_base(id)
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

@app.route("/listar_equipos", methods=["GET"])
def listar_equipos():
    conn, cursor = conectar_db()
    cursor.execute("SELECT id, base_id, tag FROM equipos")
    filas = cursor.fetchall()
    conn.close()

    equipos = []
    for fila in filas:
        equipos.append({
            "id": fila[0],
            "base_id": fila[1],
            "tag": fila[2]
        })

    return jsonify(equipos)



@app.route("/crear_equipo", methods=["POST"])
def crear_equipo():
    data = request.json

    if not data or "base_id" not in data or "tag" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    conn, cursor = conectar_db()

    # Verificar que exista el equipo base
    cursor.execute(
        "SELECT id FROM equipos_base WHERE id = ?",
        (data["base_id"],)
    )
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Equipo base no existe"}), 404

    cursor.execute(
        "INSERT INTO equipos (base_id, tag) VALUES (?, ?)",
        (data["base_id"], data["tag"])
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": nuevo_id,
        "mensaje": "Equipo creado correctamente"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

