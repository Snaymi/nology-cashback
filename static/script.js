const form = document.getElementById("cashbackForm");
const resultadoDiv = document.getElementById("resultado");
const historicoDiv = document.getElementById("historico");

function formatarMoeda(valor) {
  return Number(valor).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

function mostrarMensagemResultado(mensagem) {
  resultadoDiv.classList.remove("escondido");
  resultadoDiv.innerHTML = `<strong>Atenção:</strong> ${mensagem}`;
}

function validarFormulario(tipoCliente, valorProduto, percentualDesconto) {
  if (!["comum", "vip"].includes(tipoCliente)) {
    return "Tipo de cliente inválido.";
  }

  if (valorProduto === "") {
    return "Informe o valor do produto.";
  }

  if (!Number.isFinite(Number(valorProduto)) || Number(valorProduto) <= 0) {
    return "O valor do produto deve ser maior que zero.";
  }

  if (
    percentualDesconto === "" ||
    !Number.isFinite(Number(percentualDesconto)) ||
    Number(percentualDesconto) < 0 ||
    Number(percentualDesconto) > 100
  ) {
    return "O desconto deve estar entre 0 e 100.";
  }

  return "";
}

async function carregarHistorico() {
  try {
    const resposta = await fetch("/api/historico");

    if (!resposta.ok) {
      historicoDiv.innerHTML =
        "<p>Não foi possível carregar o histórico agora. Tente novamente em alguns segundos.</p>";
      return;
    }

    const historico = await resposta.json();

    if (historico.length === 0) {
      historicoDiv.innerHTML = "<p>Nenhuma consulta realizada ainda.</p>";
      return;
    }

    historicoDiv.innerHTML = historico
      .map((item) => {
        const tipoCliente = item.tipo_cliente === "vip" ? "VIP" : "Comum";
        const promocao = item.promocao_aplicada ? "Sim" : "Não";

        return `
          <div class="item-historico">
            <p><strong>Data:</strong> ${item.criado_em}</p>
            <p><strong>Cliente:</strong> ${tipoCliente}</p>
            <p><strong>Valor do produto:</strong> ${formatarMoeda(item.valor_produto)}</p>
            <p><strong>Desconto:</strong> ${item.percentual_desconto}%</p>
            <p><strong>Valor final:</strong> ${formatarMoeda(item.valor_final_compra)}</p>
            <p><strong>Promoção acima de R$ 500 aplicada?</strong> ${promocao}</p>
            <p><strong>Cashback:</strong> ${formatarMoeda(item.cashback_total)}</p>
          </div>
        `;
      })
      .join("");
  } catch (erro) {
    historicoDiv.innerHTML =
      "<p>Não foi possível carregar o histórico agora. Tente novamente em alguns segundos.</p>";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const tipoCliente = document.getElementById("tipoCliente").value;
  const valorProduto = document.getElementById("valorProduto").value;
  const percentualDesconto = document.getElementById("percentualDesconto").value;
  const erroValidacao = validarFormulario(
    tipoCliente,
    valorProduto,
    percentualDesconto
  );

  if (erroValidacao) {
    mostrarMensagemResultado(erroValidacao);
    return;
  }

  try {
    const resposta = await fetch("/api/cashback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        tipo_cliente: tipoCliente,
        valor_produto: valorProduto,
        percentual_desconto: percentualDesconto,
      }),
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
      mostrarMensagemResultado(
        dados.erro ||
          "Não foi possível calcular o cashback agora. Tente novamente em alguns segundos."
      );
      return;
    }

    const tipoClienteTexto = dados.tipo_cliente === "vip" ? "VIP" : "Comum";
    const promocao = dados.promocao_aplicada ? "Sim" : "Não";

    resultadoDiv.classList.remove("escondido");
    resultadoDiv.innerHTML = `
      <h3>Resultado do cálculo</h3>
      <p><strong>Tipo de cliente:</strong> ${tipoClienteTexto}</p>
      <p><strong>Valor do produto:</strong> ${formatarMoeda(dados.valor_produto)}</p>
      <p><strong>Desconto:</strong> ${dados.percentual_desconto}%</p>
      <p><strong>Valor do desconto:</strong> ${formatarMoeda(dados.valor_desconto)}</p>
      <p><strong>Valor final da compra:</strong> ${formatarMoeda(dados.valor_final_compra)}</p>
      <p><strong>Cashback base:</strong> ${formatarMoeda(dados.cashback_base)}</p>
      <p><strong>Bônus VIP:</strong> ${formatarMoeda(dados.bonus_vip)}</p>
      <p><strong>Promoção acima de R$ 500 aplicada?</strong> ${promocao}</p>
      <p><strong>Cashback final:</strong> ${formatarMoeda(dados.cashback_total)}</p>
    `;

    await carregarHistorico();
  } catch (erro) {
    mostrarMensagemResultado(
      "Não foi possível calcular o cashback agora. Tente novamente em alguns segundos."
    );
  }
});

carregarHistorico();
