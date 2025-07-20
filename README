# 💼 Consultor Financeiro Pessoal com Inteligência Artificial

Este projeto propõe uma **consultoria financeira personalizada**, combinando o poder da **Inteligência Artificial (modelos Gemini, da Google)** com a biblioteca **Agno**. O sistema coleta o perfil financeiro do usuário por meio de uma interface gráfica intuitiva, realiza análises em tempo real e gera um relatório completo em formato PDF, oferecendo orientações práticas e personalizadas para investimentos.

---

## 🎯 Objetivo

Desenvolver um sistema capaz de:

- **Captar informações financeiras e objetivos do usuário** por meio de uma interface gráfica simples e acessível.
- Utilizar um **agente principal de IA (`finance_agent`)** para:
  - Analisar o perfil do investidor de forma aprofundada.
  - Coletar **dados financeiros atualizados e detalhados** sobre ações e FIIs (preços, fundamentos, dividendos, notícias).
  - Realizar **análises comparativas** com empresas líderes do setor.
  - Sugerir um **plano mensal de alocação de capital** (valores em R$ e percentuais para ações, FIIs, renda fixa/reserva de emergência).
  - Estimar **prazos realistas para alcance dos objetivos financeiros**, considerando curto, médio e longo prazo.
  - Elaborar um **plano de ação estruturado**, com etapas claras, destacando riscos, disciplina e consistência.
- Aplicar um **agente de refinamento (`report_refiner_agent`)** para revisar e formatar a análise, garantindo que o relatório final seja **claro, bem escrito e profissional**.
- Gerar o relatório final em **formato PDF**, pronto para leitura e consulta.

---

## 🧠 Tecnologias e Bibliotecas Utilizadas

- **Modelos Gemini (Google)**: Utilizados para compreensão de linguagem natural, análise de dados, raciocínio e geração textual.
- **Agno**: Biblioteca para orquestração de agentes de IA, integração de ferramentas externas e execução de fluxos de trabalho complexos.
- **YFinanceTools (via Agno)**: Consulta dados do Yahoo Finance (preços, fundamentos, indicadores, recomendações e notícias).
- **Tkinter**: Biblioteca nativa do Python usada para a criação da interface gráfica de entrada de dados.
- **ReportLab**: Responsável pela geração e formatação do relatório final em PDF.
- **python-dotenv**: Carregamento seguro de variáveis sensíveis (como chaves de API) a partir de um arquivo `.env`.
- **re (expressões regulares)**: Usado para tratar strings e converter o texto gerado para um formato adequado à renderização do PDF.
- **os**: Manipulação de arquivos e diretórios.
- **time**: Controle de pausas durante a execução.
- **textwrap.dedent**: Auxilia na formatação limpa de blocos de texto.
- **datetime**: Manipulação de datas e horas, especialmente para marcação temporal dos relatórios.

---

## 📁 Estrutura do Projeto

```
consultor_financeiro_pessoal_ia/
├── agent.py               # Responsável pela lógica principal, criação dos agentes e geração do relatório.
├── interface_perfil.py    # Interface gráfica (Tkinter) para entrada dos dados do usuário.
├── .env                   # Armazena sua chave de API do Gemini (nunca versionar este arquivo).
└── README.md              # Documentação do projeto.
```

---

## ⚙️ Dependências

Para garantir o funcionamento adequado do projeto, instale as seguintes bibliotecas. Recomendamos o uso de um ambiente virtual para manter as dependências isoladas:

### 📦 Instalação

```bash
# 1. Crie e ative um ambiente virtual
python -m venv .venv

# No Windows:
.\.venv\Scripts\activate

# No macOS/Linux:
source .venv/bin/activate

# 2. Instale as dependências do projeto
pip install agno python-dotenv reportlab yfinance
```

> ⚠️ **Nota sobre o Tkinter**:  
> Tkinter já vem incluso na maioria das distribuições do Python.  
> No Linux, se necessário, instale com:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🚀 Como Usar

### 1. Obtenha sua Chave de API do Gemini
- Acesse o [Google AI Studio](https://makersuite.google.com/).
- Gere uma chave por meio da opção “Get API key”.
- Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave:
  ```
  GOOGLE_API_KEY=SUA_CHAVE_DE_API_AQUI
  ```
> ⚠️ **Importante**: Nunca compartilhe esse arquivo nem o inclua em repositórios públicos.

---

### 2. Execute o Projeto

No terminal (com o ambiente virtual ativado), execute:

```bash
python agent.py
```

Uma janela será exibida com o formulário para preenchimento do seu perfil financeiro. Insira seus dados com atenção.

> ✅ Para ações e FIIs brasileiros (B3), utilize o sufixo `.SA` nos tickers, por exemplo:  
> `ITUB4.SA (3612.12 reais investidos)` ou `MXRF11.SA (996 reais investidos)`.

---

### 3. Geração do Relatório

Após o envio dos dados, o sistema:

- Realiza a análise do perfil.
- Busca informações financeiras em tempo real.
- Refina e estrutura o conteúdo.
- Gera um PDF chamado `Relatorio_Financeiro_Personalizado.pdf` na pasta do projeto.

Esse processo pode levar de alguns segundos a poucos minutos, dependendo da complexidade do seu perfil e do uso da API.

---

### ✅ Resultado Final

O arquivo PDF gerado contém:

- Diagnóstico financeiro personalizado.
- Plano de investimento por categoria.
- Sugestões práticas e objetivos por horizonte de tempo.
- Recomendações com base em dados atualizados.

Abra o arquivo PDF e tenha acesso a uma consultoria financeira inteligente, acessível e feita sob medida para você.

### OBSERVAÇÃO 

Existe um sleep de 60 segundo no meio da execução dos agentes para que não ocorra o estouro da quantidade de tokens que o modelo permite, caso você não precise lidar com essa limitação REMOVA e lembresse de alterar o modelo que esta sendo utilizado!

---

