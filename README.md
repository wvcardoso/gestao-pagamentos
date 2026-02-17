# 📊 gestao-pagamentos

O **gestao-pagamentos** é um aplicativo desenvolvido para ajudar no controle de contas mensais, como energia, água, telefone e outros pagamentos recorrentes.

A ideia é centralizar todas as contas em um único lugar, permitindo:

- 📄 Leitura automática de contas em PDF
- 📝 Suporte a contas manuais via arquivo TXT
- 🏠 Identificação de residência
- 💾 Armazenamento em banco SQLite
- 📊 Visualização via dashboard web
- 💳 Suporte a pagamentos via código de barras e PIX (QR Code)

---

# 🚀 Como funciona

O sistema processa arquivos colocados na pasta de entrada:

- PDFs (contas oficiais)
- TXT (contas manuais)

Após o processamento:

- Os dados são extraídos
- A residência é identificada
- As informações são salvas no banco
- Os arquivos são movidos para a pasta de processados

---

# 📝 Formato do arquivo TXT

Para contas manuais, utilize o seguinte padrão:

```txt
tipo: pix
favorecido: <nome>
unidade_consumidora: <unidade>
vencimento: 01/01/2026
valor: 100,00
referencia: FEV/2026
pix: 999999999-99
descricao: "conta de agua"
```

# 🏠 Identificação da residência

A identificação da residência é feita com base na `unidade_consumidora`.

O sistema utiliza um arquivo `residencias.json` com o seguinte formato:

```json
{
  "endereco_01": {
    "nome": "Endereço 01",
    "energia": "xxxxxxx-1",
    "agua": "xxxxxxx-8"
  },
  "chacara": {
    "nome": "Chacara Rod 360",
    "energia": "xxxxxxx-4",
    "agua": "xxxxxxx-2"
  },
  "kit_101": {
    "nome": "Kit 101 - São Paulo",
    "energia": "xxxxxxx-5"
  }
}
```

Esse mapeamento permite relacionar contas de diferentes serviços (energia, água, etc.) à mesma residência.

# 📦 Pré-requisitos

* Python 3.10+
* pip

Instalar dependências:

```bash
pip install -r requirements.txt
```

# ▶️ Como usar

## 🔹 1. Adicionar arquivos
Coloque os arquivos na pasta:
```bash
data/entrada/
```
## 🔹 2. Processar contas
```bash
python3 app/main.py
```
## 🔹 3. Iniciar dashboard
```bash
python3 app/web.py
```

Acesse no navegador:
```bash
http://localhost:5000
```
# 📊 Funcionalidades

- ✅ Leitura de PDFs de contas
- ✅ Parser para múltiplos fornecedores
- ✅ Suporte a contas manuais (TXT) 
- ✅ Identificação de residência 
- ✅ Armazenamento em SQLite 
- ✅ Dashboard web 
- ✅ Marcar contas como pagas
- ✅ Suporte a PIX (QR Code)

# 🧠 Estrutura do projeto
```bash
app/
 ├── main.py
 ├── web.py
 ├── config.py
 ├── database.py
 ├── parser/
 └── utils/

data/
 ├── entrada/
 ├── processados/
 ├── erro/
 ├── contas.db
 └── residencias.json
 ```

# 🚀 Próximos passos (ideias)

- 📊 Gráficos de gastos por mês
- 📈 Relatórios por residência
- 🔍 Filtros no dashboard
- 🔐 Autenticação
- ☁️ Deploy em nuvem
- 📌 Observações

Este projeto foi desenvolvido com foco em automação pessoal e aprendizado, podendo evoluir para uma solução mais robusta.

# 👨‍💻 Autor
Willian (wvcardoso)