from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import os

from config import DB_FILE, SECRET_KEY, USUARIO, SENHA_HASH
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = SECRET_KEY

# 🔒 CONFIG DE SEGURANÇA (produção)
ENV = os.getenv("ENV", "dev")

app.config.update(
    SESSION_COOKIE_SECURE=(ENV == "prod"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)


# 🔹 DB
def get_contas():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contas ORDER BY vencimento")
    colunas = [col[0] for col in cursor.description]

    contas = []
    for row in cursor.fetchall():
        contas.append(dict(zip(colunas, row)))

    conn.close()
    return contas


# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USUARIO and check_password_hash(SENHA_HASH, password):
            session["logado"] = True
            return redirect(url_for("index"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


# 🔐 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# 🛡️ PROTEÇÃO
def usuario_logado():
    return session.get("logado")


# 🏠 DASHBOARD
@app.route("/")
def index():

    # 🔐 proteção
    if not usuario_logado():
        return redirect(url_for("login"))

    status = request.args.get("status")
    residencia = request.args.get("residencia")

    contas = get_contas()

    # 🔍 filtro por status
    if status:
        contas = [c for c in contas if c["status"] == status]

    # 🔍 filtro por residência
    if residencia:
        contas = [c for c in contas if c["residencia"] == residencia]

    # 🔥 lista única de residências
    residencias = sorted(set(c["residencia"] for c in get_contas() if c["residencia"]))

    total_pendente = sum(c["valor"] for c in contas if c["status"] == "pendente")
    total_pago = sum(c["valor"] for c in contas if c["status"] == "pago")
    total_contas = len(contas)

    return render_template(
        "index.html",
        contas=contas,
        total_pendente=total_pendente,
        total_pago=total_pago,
        total_contas=total_contas,
        status_selecionado=status,
        residencia_selecionada=residencia,
        residencias=residencias
    )


# 💰 PAGAR
@app.route("/pagar/<int:id>")
def pagar(id):

    # 🔐 proteção
    if not usuario_logado():
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("UPDATE contas SET status = 'pago' WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# 🚀 RUN
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )
