# Desafio Nology — Calculadora de Cashback

Projeto desenvolvido para o desafio de estágio em desenvolvimento da Nology.

## Link do app

https://nology-cashback.onrender.com

## Descrição

Este projeto consiste em uma calculadora de cashback para uma fintech. O sistema aplica as regras de negócio informadas no desafio:

* O cashback é calculado sobre o valor final da compra, após descontos.
* O cashback base é de 5%.
* Clientes VIP recebem 10% de bônus adicional sobre o cashback base.
* Compras com valor final acima de R$ 500,00 recebem o dobro de cashback.
* Cada consulta é registrada pelo IP do usuário.
* O histórico exibido mostra apenas as consultas realizadas pelo mesmo IP.

## Tecnologias utilizadas

* Python
* Flask
* SQLAlchemy
* PostgreSQL
* HTML
* CSS
* JavaScript
* Render
* Neon Postgres

## Estrutura do projeto

```txt
.
├── app.py
├── cashback.py
├── requirements.txt
├── static
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## Como executar localmente

1. Clone o repositório:

```bash
git clone LINK_DO_REPOSITORIO
```

2. Acesse a pasta do projeto:

```bash
cd NOME_DA_PASTA
```

3. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Git Bash:

```bash
source .venv/Scripts/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Configure a variável de ambiente `DATABASE_URL` em um arquivo `.env`.

Exemplo usando Postgres local:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nology_cashback
```

6. Execute o projeto:

```bash
python app.py
```

7. Acesse no navegador:

```txt
http://localhost:5000
```

## Endpoints

### GET /

Retorna a página principal da aplicação.

### GET /health

Verifica se a API está online.

### POST /api/cashback

Calcula o cashback e salva a consulta no banco de dados.

Exemplo de body:

```json
{
  "tipo_cliente": "vip",
  "valor_produto": 600,
  "percentual_desconto": 20
}
```

### GET /api/historico

Retorna o histórico de consultas feitas pelo mesmo IP do usuário.

## Autor

Snaymi Borges dos Santos Flora
