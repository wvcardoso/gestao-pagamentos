
import requests
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from app.core.settings import settings
from app.core.helper import api_post, api_get

# 🔥 cria app PRIMEIRO
web = Flask(__name__)
web.secret_key = settings.SECRET_KEY

# 🔐 LOGIN
@web.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")       

        # DEBUG
        #print(f"USUARIO: {USUARIO}")
        #print(f"password: {password}")
        #print(f"SENHA_HASH: {SENHA_HASH}")
        #print(f"check_password_hash result: {check_password_hash(SENHA_HASH, password)}")

        if username == settings.USUARIO and check_password_hash(settings.SENHA_HASH, password):            
            session["logado"] = True
            session["usuario"] = username
            return redirect(url_for("index"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")

# 🔐 LOGOUT
@web.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Pagar conta
@web.route("/pagar/<int:id>")
def pagar(id):

    if not session.get("logado"):
        return redirect(url_for("login"))

    try:
        api_post(f"contas/pagar/{id}")
    except Exception as e:
        print("Erro ao pagar:", e)

    return redirect(url_for("index"))

# Index
@web.route("/")
def index():   
    
    if not session.get("logado"):
        return redirect(url_for("login"))

    status = request.args.get("status")
    residencia = request.args.get("residencia")
    periodo = request.args.get("periodo")

    try:        
        response = api_get(f"contas/")
        response.raise_for_status()
        contas = response.json()

        if not isinstance(contas, list):
            print("API retornou algo inesperado:", contas)
            contas = []

    except Exception as e:
        print("Erro ao chamar API:", e)
        contas = []

    # 🔍 filtros
    if status:
        contas = [c for c in contas if c.get("status") == status]

    if residencia:
        contas = [c for c in contas if c.get("residencia") == residencia]

    if periodo:
        contas = [
            c for c in contas
            if c.get("vencimento") and c.get("vencimento")[3:10] == periodo
        ]

    # 🔥 listas auxiliares
    residencias = sorted(set(
        c.get("residencia") for c in contas if c.get("residencia")
    ))

    periodos = sorted(set(
        c.get("vencimento")[3:10]
        for c in contas
        if c.get("vencimento")
    ), reverse=True)

    mapa_meses = {
        "01": "Jan", "02": "Fev", "03": "Mar",
        "04": "Abr", "05": "Mai", "06": "Jun",
        "07": "Jul", "08": "Ago", "09": "Set",
        "10": "Out", "11": "Nov", "12": "Dez"
    }

    # 🔢 totais
    total_pendente = sum(c.get("valor", 0) for c in contas if c.get("status") == "pendente")
    total_pago = sum(c.get("valor", 0) for c in contas if c.get("status") == "pago")
    total_contas = len(contas)

    return render_template(
        "index.html",
        contas=contas,
        total_pendente=total_pendente,
        total_pago=total_pago,
        total_contas=total_contas,
        status_selecionado=status,
        residencia_selecionada=residencia,
        periodo_selecionado=periodo,
        residencias=residencias,
        periodos=periodos,
        mapa_meses=mapa_meses
    )

# 🚀 rodar web
if __name__ == "__main__":
    web.run(host="0.0.0.0", debug=True, port=5000)