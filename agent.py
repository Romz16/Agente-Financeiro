import os
from textwrap import dedent
from datetime import datetime  
from dotenv import load_dotenv
import re
import time
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from interface_perfil import run_profile_app

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

# --- AGENTE FINANCEIRO INTELIGENTE  ---
finance_agent = Agent(
    model=Gemini(id="gemini-1.5-flash"),  
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            historical_prices=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=dedent(
        """\
Você é um **Consultor Financeiro Pessoal Exímio e um Analista de Investimentos Sênior de Wall Street**. 💼📈

Sua missão é fornecer **análises financeiras aprofundadas** e **recomendações estratégicas de investimento altamente personalizadas**, com **orientações práticas e acionáveis** sobre o que fazer com o dinheiro do usuário, com base no seu perfil financeiro e objetivos declarados.

---

### 🧠 Seu Processo de Análise e Recomendação:

#### 1. ANÁLISE COMPLETA DO PERFIL DO INVESTIDOR (CRUCIAL):
- Interprete integralmente o **"PERFIL DO INVESTIDOR"** fornecido.
- Calcule a **economia líquida mensal disponível para investir**.
- Avalie:
  - a **tolerância a risco**,
  - o **nível de conhecimento** em finanças,
  - e os **objetivos de curto, médio e longo prazo** (ex: reserva de emergência, aposentadoria, aquisição de imóveis).
- Identifique:
  - **ações de interesse atual**,
  - **setores preferidos**,
  - **preferência por renda passiva (dividendos)** ou crescimento.

#### 2. ANÁLISE DE ATIVOS DE INTERESSE E COMPARAÇÃO SETORIAL:
- Para cada **ação de interesse** mencionada no perfil do usuário:
    - **Dados Fundamentais:** Obtenha preço atual, alta/baixa 52 semanas, P/E, Market Cap, EPS, dividend yield, histórico de dividendos, notícias recentes, **Valor Patrimonial por Ação (VPA), Margens (Bruta, Líquida, EBITDA), Endividamento (Dívida Líquida/EBITDA), Fluxo de Caixa Operacional/Livre, Crescimento de Lucro (CAGR), Recomendação de Consenso de Analistas (se disponível) e Volume Médio Diário**.
    - **Performance Histórica:** Analise tendências de preços (curto, médio e longo prazo) para identificar padrões de crescimento ou desvalorização.
    - **Análise de Dividendos:** Avalie a sustentabilidade e o histórico de pagamento de dividendos, alinhando com o objetivo de renda passiva do usuário.
- **Busca e Comparação Setorial:**
    - **Identifique outras ações líderes no MESMO SETOR** das ações de interesse do usuário (ex: para PETR4, buscar outras de Energia/Petróleo; para ITSA4, buscar outros Bancos/Financeiras).
    - **Compare** as ações de interesse do usuário com essas pares do setor em termos de múltiplos de valuation (P/E, P/VP), crescimento de receita/lucro, dividendos, market share, e perspectivas futuras.
    - **Avalie a situação delas** e se **compensa migrar** ou diversificar para essas alternativas, apresentando os prós e contras de cada movimento.


#### 3. PLANO DE AÇÃO PRÁTICO PARA USO DO DINHEIRO:
- **Reserva de Emergência:** Calcule e recomende o valor restante necessário para atingir a meta da reserva de emergência e sugira a melhor alocação para esse fim (ex: Tesouro Selic, CDB de liquidez diária).
- **Alocação de Investimento Mensal:** Proponha uma **distribuição percentual detalhada da economia mensal disponível** para investir em diferentes classes de ativos (ex: ações, FIIs, renda fixa), alinhada com o perfil de risco e os objetivos (curto, médio e longo prazo).
- **QUANTO INVESTIR E QUANDO ATINGIR OBJETIVOS:**
    - **Para cada objetivo (curto, médio, longo prazo), forneça uma estimativa realista de QUANTO o usuário deve investir mensalmente e uma projeção de QUANDO ele poderá atingir esse objetivo**, considerando a economia mensal disponível, a rentabilidade esperada para cada classe de ativo e o prazo.
    - **Detalhe a alocação específica em R$ para Ações, Fundos Imobiliários (FIIs) e Renda Fixa/Reserva**, baseando-se na economia mensal e na alocação percentual.
- **Recomendações Específicas para Ações de Interesse:**
    - Para cada ação: Forneça uma **recomendação clara (Comprar, Vender, Manter)**, justificada por dados e sua análise.
    - **Quanto Comprar/Vender:** Se for uma recomendação de compra, sugira um **valor em reais** ou uma **quantidade aproximada** de ações para alocar, considerando a alocação percentual e o capital disponível.
    - **Estratégia de Venda:** Se houver recomendações de venda, explique os gatilhos ou condições para realizar a venda.


#### 4. ALOCAÇÃO DE INVESTIMENTOS MENSAIS E ESTRATÉGIA:
- Proponha uma **distribuição percentual clara e equilibrada** da economia mensal entre classes de ativos (ações, FIIs, renda fixa, reserva).
- Para cada classe, indique:
  - **quantia em reais a ser alocada** mensalmente,
  - e **quais ativos específicos adquirir** com esse valor.
- Utilize o perfil do usuário para calibrar o risco e potencial de retorno da carteira.
- Baseado nos objetivos de longo prazo (ex: aposentadoria), crie um **plano de etapas/passos acionáveis** que o usuário deve seguir.
- Inclua a importância da **diversificação**, **rebalanceamento de carteira** e **reinvestimento de dividendos**.
- Ofereça **metas anuais ou trimestrais** que ajudem o usuário a monitorar seu progresso.
- Mencione estratégias para lidar com a inflação e a volatilidade do mercado.


#### 5. PLANEJAMENTO DE LONGO PRAZO:
- Elabore um **plano estratégico em etapas**, com:
  - **Metas anuais ou trimestrais**,
  - Sugestões de **reinvestimento de dividendos**,
  - Estratégias de defesa contra **inflação e volatilidade**,
  - Regras práticas para diversificação e acompanhamento do portfólio.
- Inclua, quando relevante, **simulações de crescimento patrimonial** com base nos aportes mensais recomendados.

---

### 📄 Formato do Relatório (OBRIGATÓRIO):
- Inicie com um **🔎 RESUMO EXECUTIVO**, destacando:
  - principais recomendações,
  - alocações sugeridas,
  - decisões de compra/venda.
- Use **Markdown com cabeçalhos** `##`, `###` para clareza.
- Apresente **dados financeiros e comparações em TABELAS Markdown** sempre que possível.
- Utilize **emojis** (📈📉💰💼⭐📊) para destacar pontos críticos.
- Destaque **recomendações específicas** com bullets `-`.
- **Explique qualquer termo técnico de forma concisa e objetiva.**
- Finalize com um **plano de ação prático** e uma **seção de Divulgação de Riscos** obrigatória.

---

### ⚠️ AVISO LEGAL E DIVULGAÇÃO DE RISCOS (OBRIGATÓRIO):
- Este relatório é gerado por uma inteligência artificial e se destina exclusivamente a fins **informativos e educacionais**. Não constitui consultoria financeira, jurídica ou fiscal personalizada.
- Investimentos em renda variável envolvem riscos, incluindo a perda parcial ou total do capital investido.
- Rentabilidade passada **não garante** rentabilidade futura.
- As condições de mercado são voláteis. Consulte sempre um **profissional certificado** antes de tomar decisões de investimento.
- **Diversificação e disciplina são fundamentais** para a mitigação de riscos.
"""
    ),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

# Este agente receberá a saída do agente principal e a reformulará para o formato final.
report_refiner_agent = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    instructions=dedent(
        """\
        Você é um **Editor Sênior de Relatórios Financeiros e Especialista em Comunicação Corporativa**. 📝✨
        Sua tarefa é receber um rascunho de análise financeira e transformá-lo em um relatório final **único, bem escrito, conciso, e com linguagem profissional, mas fácil de compreender** para um investidor.

        **Siga estas diretrizes rigorosas:**
        1.  **Concisão e Clareza:** Remova redundâncias. Sintetize informações complexas em parágrafos claros e diretos.
        2.  **Linguagem:** Adote um tom profissional, mas acessível. Evite jargões desnecessários ou explique-os de forma simples. Use voz ativa.
        3.  **Estrutura:** Mantenha a estrutura de cabeçalhos Markdown (##, ###) e tabelas. Garanta um fluxo lógico de informações.
        4.  **Tópicos Obrigatórios:** Certifique-se de que o relatório final cubra **TODOS** os seguintes pontos, de forma integrada:
            - Análise do perfil do investidor (contexto).
            - Análise das ações de interesse (desempenho, dividendos, recomendações com valores/quantidades).
            - Comparação detalhada com outras ações do mesmo setor (com prós/contras de migração/diversificação).
            - Plano de alocação de capital da economia mensal disponível.
            - Roteiro claro de longo prazo com etapas acionáveis.
        5.  **Tom:** Seja informativo e direto. Evite suposições e mantenha o foco na análise baseada em dados.
        6.  **Disclaimers:** O relatório final **DEVE** incluir uma seção clara de "Aviso Legal e Divulgação de Riscos" no final, com o conteúdo que você já conhece sobre a natureza informativa e os riscos dos investimentos.

        Seu output deve ser o relatório final completo, pronto para ser apresentado.
        """
    ),
    add_datetime_to_instructions=False,
    show_tool_calls=False,
    markdown=True,
)


# --- FUNÇÃO DE EXPORTAÇÃO PARA PDF ---
def export_to_pdf(text_content, filename="relatorio_financeiro.pdf"):
    """
    Converte um texto Markdown (com tabelas e cabeçalhos simples) em um arquivo PDF.
    """
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    styles["h1"].fontName = "Helvetica-Bold"
    styles["h1"].fontSize = 18
    styles["h1"].spaceAfter = 14

    styles["h2"].fontName = "Helvetica-Bold"
    styles["h2"].fontSize = 14
    styles["h2"].spaceAfter = 10

    styles["Normal"].fontName = "Helvetica"
    styles["Normal"].fontSize = 10
    styles["Normal"].leading = 12
    styles["Normal"].alignment = TA_JUSTIFY

    styles.add(
        ParagraphStyle(
            name="CustomListItem",
            fontName="Helvetica",
            fontSize=10,
            leading=12,
            leftIndent=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CustomTableText",
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            alignment=TA_JUSTIFY,
        )
    )

    story = []
    lines = text_content.split("\n")
    in_table = False
    table_data = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("|") and "|" in stripped_line[1:]:
            if not in_table:
                in_table = True
                table_data = []
            row = [
                Paragraph(
                    cell.strip().replace("- ", "<br/>- "), styles["CustomTableText"]
                )
                for cell in stripped_line.split("|")
                if cell.strip()
            ]
            if row:
                table_data.append(row)
            continue
        elif in_table:  
            in_table = False
            if table_data:
                num_cols = len(table_data[0]) if table_data else 0
                if num_cols > 0:
                    table_style = TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 4),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                            ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        ]
                    )
                    if len(table_data) > 1 and all(
                        isinstance(c, Paragraph) and "-" in c.text
                        for c in table_data[1]
                    ):
                        table_data = [table_data[0]] + table_data[2:]

                    table_obj = Table(
                        table_data,
                        colWidths=(
                            [doc.width / num_cols] * num_cols if num_cols > 0 else None
                        ),
                    )
                    table_obj.setStyle(table_style)
                    story.append(table_obj)
                    story.append(Spacer(1, 0.2 * cm))
            table_data = []

        if stripped_line.startswith("## "):
            story.append(Paragraph(stripped_line[3:].strip(), styles["h1"]))
            story.append(Spacer(1, 0.2 * cm))
        elif stripped_line.startswith("### "):
            story.append(Paragraph(stripped_line[4:].strip(), styles["h2"]))
            story.append(Spacer(1, 0.1 * cm))

        elif stripped_line.startswith("- "):
            story.append(Paragraph(stripped_line, styles["CustomListItem"]))
        
        elif stripped_line:
            formatted_line = line
            formatted_line = re.sub(
                r"\*\*(.*?)\*\*", r"<b>\1</b>", formatted_line
            )  # Negrito
            formatted_line = re.sub(
                r"\*(.*?)\*", r"<i>\1</i>", formatted_line
            )  # Itálico

            story.append(Paragraph(formatted_line, styles["Normal"]))
            if not in_table:
                story.append(Spacer(1, 0.1 * cm))
        else:
            story.append(Spacer(1, 0.1 * cm))

    doc.build(story)
    print(f"Relatório salvo como: {filename}")


# --- INÍCIO DO FLUXO PRINCIPAL ---

print("--- Abrindo interface para preenchimento do perfil ---")

profile_data = run_profile_app()

if not profile_data:
    print("Preenchimento do perfil cancelado ou falhou. Encerrando o programa.")
    exit()

data_analise = datetime.now().strftime("%Y-%m-%d")

economia_mensal_disponivel = profile_data["renda_mensal"] - profile_data["gastos_fixos"]

acoes_formatadas = profile_data["acoes_interesse"]

obj_curto_formatado = ""
if profile_data["obj_curto"].strip():
    obj_curto_formatado += f"- **Curto Prazo (até 1 ano):**\n"
    obj_curto_formatado += f"    - **Objetivo:** {profile_data['obj_curto']}\n"
    if profile_data["prazo_curto_meses"].strip():
        obj_curto_formatado += (
            f"    - **Prazo Restante:** {profile_data['prazo_curto_meses']} meses.\n"
        )

obj_medio_formatado = ""
if profile_data["obj_medio"].strip():
    obj_medio_formatado += f"- **Médio Prazo (1 a 5 anos):**\n"
    obj_medio_formatado += f"    - **Objetivo:** {profile_data['obj_medio']}\n"
    if profile_data["prazo_medio_anos"].strip():
        obj_medio_formatado += (
            f"    - **Prazo:** {profile_data['prazo_medio_anos']} anos.\n"
        )


meu_perfil_investidor_formatado = dedent(
    f"""
### PERFIL DO INVESTIDOR

**1. Informações Básicas:**
- **Nome:** {profile_data["nome"]}
- **Data da Análise:** {data_analise}

**2. Situação Financeira Atual:**
- **Renda Líquida Mensal:** R$ {profile_data["renda_mensal"]:.2f}
- **Gastos Fixos Mensais:** R$ {profile_data["gastos_fixos"]:.2f}
- **Economia Mensal Disponível para Investimento:** R$ {economia_mensal_disponivel:.2f}
- **Reservas Atuais de Emergência:** R$ {profile_data["reservas_emergencia"]:.2f}

**3. Perfil de Risco e Conhecimento:**
- **Tolerância a Risco:** {profile_data["tolerancia_risco"]}
- **Nível de Conhecimento em Investimentos:** {profile_data["nivel_conhecimento"]}

**4. Objetivos de Investimento:**
{obj_curto_formatado}{obj_medio_formatado}- **Longo Prazo (5+ anos)::**
    - **Objetivo Principal:** {profile_data["obj_longo"]}
    - **Objetivo Secundário:** Garantir crescimento de capital para cobrir a inflação.

**5. Interesses e Preferências de Investimento:**
- **Ações Atuais de Interesse/Posse:** {acoes_formatadas}.
- **Setores de Interesse:** {profile_data["setores_interesse"]}.
- **Preferência de Renda:** {profile_data["pref_renda"]}.
- **Outras Considerações:** {profile_data["outras_consideracoes"] if profile_data["outras_consideracoes"] else "N/A"}.
"""
)


prompt_para_analise = dedent(
    f"""\
    Com base no meu PERFIL DO INVESTIDOR abaixo, por favor, gere um relatório de consultoria financeira **MUITO DETALHADO, ABRANGENTE E REALISTA**.
    O relatório deve ser uma análise estratégica aprofundada que cubra todos os pontos solicitados com especificidade e insights práticos.

    Seu relatório deve conter as seguintes seções obrigatórias:

    **1. Análise Aprofundada das Ações de Interesse:**
        - Para cada ação atual ({acoes_formatadas}): # <--- LINHA CORRIGIDA AQUI!
          - Desempenho recente (últimos 12 meses, 3 anos, 5 anos) e projeções.
          - Análise completa de dividendos (histórico de pagamentos, dividend yield atual, sustentabilidade do dividendo).
          - Recomendações claras (Comprar, Vender, Manter) com justificativas sólidas baseadas em dados fundamentalistas e técnicos.
          - Sugestão precisa de valores ou quantidades para comprar/vender, considerando meu perfil e valor investido.

    **2. Comparativo Setorial e Oportunidades de Migração:**
        - Para cada ação de interesse, identifique **pelo menos 3 a 5 outras empresas líderes do MESMO SETOR** (ex: outros grandes bancos para ITUB4.SA, outras empresas de energia ou siderurgia para GOAU4.SA, outros FIIs para GARE11.SA).
        - Apresente uma **tabela comparativa exaustiva** com métricas financeiras chave (P/L, P/VP, dívida/EBITDA, ROE, crescimento de receita, dividend yield, VPA, Margens, Endividamento, Fluxo de Caixa, Crescimento de Lucro, Recomendação de Consenso, Volume Médio Diário) e notícias relevantes.
        - Com base nessa comparação e no meu perfil, **avalie EXPLICITAMENTE se compensa migrar** (parcial ou totalmente) ou diversificar para essas empresas alternativas. Forneça os prós e contras específicos de cada ação, e o impacto potencial nos meus objetivos.

    **3. Planejamento de Alocação de Capital Mensal (Curto, Médio e Longo Prazo):**
        - Dada a minha economia mensal disponível (R$ {economia_mensal_disponivel:.2f}), detalhe um **plano de alocação percentual** para cada um dos meus objetivos:
          - **Curto Prazo:** Como alcançar a reserva de emergência e os objetivos de curto prazo, com sugestões de produtos específicos (ex: Tesouro Selic, CDB de liquidez diária) e o tempo estimado.
          - **Médio Prazo:** Como planejar os objetivos de médio prazo (ex: apartamento), com alocação em investimentos adequados ao prazo e risco.
          - **Longo Prazo:** Qual a estratégia de alocação para longo prazo, detalhando percentuais para ações, FIIs e outras classes de ativos.
        - **Para cada objetivo (curto, médio, longo prazo), forneça uma estimativa realista de QUANTO o usuário deve investir mensalmente e uma projeção de QUANDO ele poderá atingir esse objetivo**, considerando a economia mensal disponível, a rentabilidade esperada para cada classe de ativo e o prazo.
        - **Detalhe a alocação específica em R$ para Ações, Fundos Imobiliários (FIIs) e Renda Fixa/Reserva**, baseando-se na economia mensal e na alocação percentual.
        - Justifique cada alocação com base nos objetivos, tolerância a risco e cenário de mercado.

    **4. Roteiro de Investimento e Desafios (Curto e Longo Prazo):**
        - Forneça um **roteiro claro, etapa por etapa**, para atingir meus objetivos de **curto e longo prazo**.
        - **Curto Prazo:** Ações imediatas a tomar (ex: abrir conta em corretora, aportar na reserva).
        - **Longo Prazo:** Estratégias de investimento contínuas, marcos anuais/trimestrais, reinvestimento de dividendos, rebalanceamento de carteira.
        - **Dificuldades e Realismo:**
          - Discuta as **dificuldades e desafios inerentes** a cada objetivo e estratégia (ex: volatilidade do mercado, inflação, taxas, impostos, liquidez).
          - Seja **realista** sobre os prazos e retornos esperados, sem prometer ganhos fáceis.
          - Aborde a importância da **disciplina**, **paciência** e **educação financeira contínua**.
          - Mencione a necessidade de **acompanhamento constante** do mercado e adaptação da estratégia.

    **5. Conclusão e Próximos Passos:**
        - Resumo das principais recomendações e um chamado à ação para o investidor.
    {meu_perfil_investidor_formatado}

"""
)

print("--- INICIANDO ANÁLISE INICIAL DETALHADA ---")

analise_bruta_completa = ""
try:
    for chunk in finance_agent.run(prompt_para_analise, stream=True):
        content = getattr(chunk, "content", "")
        if isinstance(content, str) and content.strip():
            analise_bruta_completa += content
except Exception as e:
    print(f"\nERRO na execução do finance_agent: {e}")
    if "RESOURCE_EXHAUSTED" in str(e):
        print(
            "Cota da API do Gemini excedida. Por favor, aguarde e tente novamente, ou considere usar o modelo 'flash' ou habilitar o faturamento."
        )
    exit()


print("\n--- INICIANDO REFINAMENTO E FORMATAÇÃO DO RELATÓRIO FINAL ---")
prompt_para_refinamento = dedent(
    f"""\
    Por favor, refine e formate o seguinte rascunho de análise financeira em um relatório único, conciso, profissional e fácil de compreender.
    Certifique-se de que todos os pontos estejam cobertos e inclua a seção de Aviso Legal e Divulgação de Riscos que você conhece.

    RASCUNHO DA ANÁLISE FINANCEIRA:
    {analise_bruta_completa}
"""
)
print("\n--- Aguardando para evitar limite de cota... ---")
time.sleep(60)  # Pausa de 60 segundos antes de chamar o próximo agente


output_lines_final = []
relatorio_final_texto = ""
try:
    for chunk in report_refiner_agent.run(prompt_para_refinamento, stream=True):
        content = getattr(chunk, "content", "")
        if isinstance(content, str) and content.strip():
            relatorio_final_texto += content
except Exception as e:
    print(f"\nERRO na execução do report_refiner_agent: {e}")
    if "RESOURCE_EXHAUSTED" in str(e):
        print(
            "Cota da API do Gemini excedida. Por favor, aguarde e tente novamente, ou considere usar o modelo 'flash' ou habilitar o faturamento."
        )
    exit()


# --- EXPORTAR PARA PDF ---
if relatorio_final_texto:
    print("\n--- EXPORTANDO RELATÓRIO PARA PDF ---")
    export_to_pdf(relatorio_final_texto, "Relatorio_Financeiro_Personalizado.pdf")
else:
    print("\nNão foi possível gerar o relatório final para exportação em PDF.")

print("\n--- PROCESSO CONCLUÍDO ---")
