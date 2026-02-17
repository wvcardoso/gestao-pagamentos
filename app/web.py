from flask import Flask, render_template, redirect, url_for
import sqlite3
from config import DB_FILE

app = Flask(__name__)


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


@app.route("/")
def index():
    contas = get_contas()
    return render_template("index.html", contas=contas)


@app.route("/pagar/<int:id>")
def pagar(id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("UPDATE contas SET status = 'pago' WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
