from decimal import Decimal, ROUND_HALF_UP


def formatar_dinheiro(valor):
    valor_formatado = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"R$ {valor_formatado:.2f}".replace(".", ",")


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
        "valor_produto": valor_produto,
        "percentual_desconto": percentual_desconto,
        "valor_desconto": valor_desconto,
        "valor_final_compra": valor_final_compra,
        "cashback_base": cashback_base,
        "bonus_vip": bonus_vip,
        "cashback_total": cashback_total,
        "cliente_vip": cliente_vip,
        "promocao_aplicada": promocao_aplicada,
    }


def exibir_resultado(numero_questao, descricao, resultado):
    tipo_cliente = "VIP" if resultado["cliente_vip"] else "Comum"
    promocao = "Sim" if resultado["promocao_aplicada"] else "Não"

    print("=" * 60)
    print(f"RESPOSTA DA QUESTÃO {numero_questao}")
    print("=" * 60)
    print(descricao)
    print("-" * 60)
    print(f"Tipo de cliente: {tipo_cliente}")
    print(f"Valor do produto: {formatar_dinheiro(resultado['valor_produto'])}")
    print(f"Percentual de desconto: {resultado['percentual_desconto']}%")
    print(f"Valor do desconto: {formatar_dinheiro(resultado['valor_desconto'])}")
    print(f"Valor final da compra: {formatar_dinheiro(resultado['valor_final_compra'])}")
    print("-" * 60)
    print(f"Cashback base: {formatar_dinheiro(resultado['cashback_base'])}")
    print(f"Bônus VIP: {formatar_dinheiro(resultado['bonus_vip'])}")
    print(f"Promoção acima de R$ 500 aplicada? {promocao}")
    print("-" * 60)
    print(f"Cashback final: {formatar_dinheiro(resultado['cashback_total'])}")
    print("=" * 60)
    print()


print("=" * 60)
print("RESPOSTA DA QUESTÃO 1")
print("=" * 60)
print("Código Python criado para calcular o cashback final conforme as regras de negócio.")
print("O cálculo considera desconto, cashback base, bônus VIP e promoção para compras acima de R$ 500.")
print()


resultado_questao_2 = calcular_cashback(
    valor_produto=600,
    percentual_desconto=20,
    cliente_vip=True
)

exibir_resultado(
    numero_questao=2,
    descricao="Cliente VIP comprando um produto de R$ 600,00 com cupom de 20% off.",
    resultado=resultado_questao_2
)


resultado_questao_3 = calcular_cashback(
    valor_produto=600,
    percentual_desconto=10,
    cliente_vip=False
)

exibir_resultado(
    numero_questao=3,
    descricao="Cliente comum comprando um produto de R$ 600,00 com cupom de 10% off.",
    resultado=resultado_questao_3
)

resultado_questao_4 = calcular_cashback(
    valor_produto=600,
    percentual_desconto=15,
    cliente_vip=True
)

exibir_resultado(
    numero_questao=4,
    descricao="Cliente VIP comprando um produto de R$ 600,00 com cupom de 15% off.",
    resultado=resultado_questao_4
)