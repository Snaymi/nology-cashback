from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

database_url = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class ConsultaCashback(db.Model):
    __tablename__ = "consultas_cashback"

    id = db.Column(db.Integer, primary_key=True)
    ip_usuario = db.Column(db.String(100), nullable=False)
    tipo_cliente = db.Column(db.String(20), nullable=False)
    valor_produto = db.Column(db.Numeric(10, 2), nullable=False)
    percentual_desconto = db.Column(db.Numeric(5, 2), nullable=False)
    valor_desconto = db.Column(db.Numeric(10, 2), nullable=False)
    valor_final_compra = db.Column(db.Numeric(10, 2), nullable=False)
    cashback_base = db.Column(db.Numeric(10, 2), nullable=False)
    bonus_vip = db.Column(db.Numeric(10, 2), nullable=False)
    cashback_total = db.Column(db.Numeric(10, 2), nullable=False)
    promocao_aplicada = db.Column(db.Boolean, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


def formatar_decimal(valor):
    return Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def obter_ip_usuario():
    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.remote_addr or "IP não identificado"


def calcular_cashback(valor_produto, percentual_desconto, cliente_vip=False):
    valor_produto = Decimal(str(valor_produto))
    percentual_desconto = Decimal(str(percentual_desconto))

    percentual_cashback_base = Decimal("0.05")
    percentual_bonus_vip = Decimal("0.10")
    limite_promocao = Decimal("500")

    valor_desconto = valor_produto * (percentual_desconto / Decimal("100"))
    valor_final_compra = valor_produto - valor_desconto

    cashback_base = valor_final_compra * percentual_cashback_base

    bonus_vip = Decimal("0")
    if cliente_vip:
        bonus_vip = cashback_base * percentual_bonus_vip

    cashback_total = cashback_base + bonus_vip

    promocao_aplicada = False
    if valor_final_compra > limite_promocao:
        cashback_total *= Decimal("2")
        promocao_aplicada = True

    return {
        "valor_produto": formatar_decimal(valor_produto),
        "percentual_desconto": formatar_decimal(percentual_desconto),
        "valor_desconto": formatar_decimal(valor_desconto),
        "valor_final_compra": formatar_decimal(valor_final_compra),
        "cashback_base": formatar_decimal(cashback_base),
        "bonus_vip": formatar_decimal(bonus_vip),
        "cashback_total": formatar_decimal(cashback_total),
        "promocao_aplicada": promocao_aplicada,
    }


def dinheiro_para_json(valor):
    return f"{Decimal(valor):.2f}"


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/cashback", methods=["POST"])
def calcular_e_salvar_cashback():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados não enviados."}), 400

    tipo_cliente = dados.get("tipo_cliente")
    valor_produto = dados.get("valor_produto")
    percentual_desconto = dados.get("percentual_desconto", 0)

    if tipo_cliente not in ["comum", "vip"]:
        return jsonify({"erro": "Tipo de cliente inválido."}), 400

    if valor_produto is None:
        return jsonify({"erro": "Valor do produto é obrigatório."}), 400

    try:
        valor_produto = Decimal(str(valor_produto))
        percentual_desconto = Decimal(str(percentual_desconto))
    except Exception:
        return jsonify({"erro": "Valor do produto ou desconto inválido."}), 400

    if valor_produto <= 0:
        return jsonify({"erro": "O valor do produto deve ser maior que zero."}), 400

    if percentual_desconto < 0 or percentual_desconto > 100:
        return jsonify({"erro": "O desconto deve estar entre 0 e 100."}), 400

    cliente_vip = tipo_cliente == "vip"
    resultado = calcular_cashback(valor_produto, percentual_desconto, cliente_vip)
    ip_usuario = obter_ip_usuario()

    consulta = ConsultaCashback(
        ip_usuario=ip_usuario,
        tipo_cliente=tipo_cliente,
        valor_produto=resultado["valor_produto"],
        percentual_desconto=resultado["percentual_desconto"],
        valor_desconto=resultado["valor_desconto"],
        valor_final_compra=resultado["valor_final_compra"],
        cashback_base=resultado["cashback_base"],
        bonus_vip=resultado["bonus_vip"],
        cashback_total=resultado["cashback_total"],
        promocao_aplicada=resultado["promocao_aplicada"],
    )

    db.session.add(consulta)
    db.session.commit()

    return jsonify({
        "tipo_cliente": tipo_cliente,
        "valor_produto": dinheiro_para_json(resultado["valor_produto"]),
        "percentual_desconto": dinheiro_para_json(resultado["percentual_desconto"]),
        "valor_desconto": dinheiro_para_json(resultado["valor_desconto"]),
        "valor_final_compra": dinheiro_para_json(resultado["valor_final_compra"]),
        "cashback_base": dinheiro_para_json(resultado["cashback_base"]),
        "bonus_vip": dinheiro_para_json(resultado["bonus_vip"]),
        "cashback_total": dinheiro_para_json(resultado["cashback_total"]),
        "promocao_aplicada": resultado["promocao_aplicada"],
    })


@app.route("/api/historico", methods=["GET"])
def listar_historico():
    ip_usuario = obter_ip_usuario()

    consultas = (
        ConsultaCashback.query
        .filter_by(ip_usuario=ip_usuario)
        .order_by(ConsultaCashback.criado_em.desc())
        .limit(20)
        .all()
    )

    historico = []

    for consulta in consultas:
        historico.append({
            "id": consulta.id,
            "tipo_cliente": consulta.tipo_cliente,
            "valor_produto": dinheiro_para_json(consulta.valor_produto),
            "percentual_desconto": dinheiro_para_json(consulta.percentual_desconto),
            "valor_final_compra": dinheiro_para_json(consulta.valor_final_compra),
            "cashback_total": dinheiro_para_json(consulta.cashback_total),
            "promocao_aplicada": consulta.promocao_aplicada,
            "criado_em": consulta.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
        })

    return jsonify(historico)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)