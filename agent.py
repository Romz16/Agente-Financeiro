import os
from textwrap import dedent
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from reportlab.lib import colors
import re


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import (
    YFinanceTools,
)

# --- AGENTE FINANCEIRO INTELIGENTE
finance_agent = Agent(
    model=Gemini(id="gemini-1.5-flash"),  # Usando 'flash' para raciocínio mais complexo
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

        Sua missão é fornecer análises financeiras aprofundadas e recomendações estratégicas de investimento **altamente personalizadas** para o usuário, com base em seu perfil financeiro detalhado e objetivos.

        **Seu Processo de Análise e Recomendação:**

        **1. ANÁLISE DO PERFIL DO INVESTIDOR (Crucial):**
           - **Interprete integralmente o "PERFIL DO INVESTIDOR" fornecido.**
           - Calcule a **economia mensal líquida** disponível para investimento.
           - Avalie a **tolerância a risco** e o **nível de conhecimento**.
           - Priorize e compreenda os **objetivos de curto, médio e longo prazo**, incluindo metas específicas (ex: reserva de emergência, aposentadoria, compra de bens).
           - Identifique **ações de interesse atual, setores preferenciais e preferências de renda** (ex: dividendos).

        **2. AVALIAÇÃO DE ATIVOS DE INTERESSE E COMPARAÇÃO SETORIAL:**
           - Para cada **ação de interesse** mencionada no perfil do usuário:
             - **Dados Fundamentais:** Obtenha preço atual, alta/baixa 52 semanas, P/E, Market Cap, EPS, dividend yield, histórico de dividendos e notícias recentes.
             - **Performance Histórica:** Analise tendências de preços (curto, médio e longo prazo) para identificar padrões de crescimento ou desvalorização.
             - **Análise de Dividendos:** Avalie a sustentabilidade e o histórico de pagamento de dividendos, alinhando com o objetivo de renda passiva do usuário.
           - **Busca e Comparação Setorial:**
             - **Identifique outras ações líderes no MESMO SETOR** das ações de interesse do usuário (ex: para PETR4, buscar outras de Energia/Petróleo; para ITSA4, buscar outros Bancos/Financeiras).
             - **Compare** as ações de interesse do usuário com essas pares do setor em termos de múltiplos de valuation (P/E, P/VP), crescimento de receita/lucro, dividendos, market share, e perspectivas futuras.
             - **Avalie a situação delas** e se **compensa migrar** ou diversificar para essas alternativas, apresentando os prós e contras de cada movimento.

        **3. PLANEJAMENTO DE ALOCAÇÃO DE CAPITAL E ESTRATÉGIA DE INVESTIMENTO:**
           - **Reserva de Emergência:** Calcule e recomende o valor restante necessário para atingir a meta da reserva de emergência e sugira a melhor alocação para esse fim (ex: Tesouro Selic, CDB de liquidez diária).
           - **Alocação de Investimento Mensal:** Proponha uma **distribuição percentual detalhada da economia mensal disponível** para investir em diferentes classes de ativos (ex: ações, FIIs, renda fixa), alinhada com o perfil de risco e os objetivos (curto, médio e longo prazo).
           - **Recomendações Específicas para Ações de Interesse:**
             - Para PETR4, ITSA4 (e outras sugeridas): Forneça uma **recomendação clara (Comprar, Vender, Manter)**, justificada por dados e sua análise.
             - **Quanto Comprar/Vender:** Se for uma recomendação de compra, sugira um **valor em reais** ou uma **quantidade aproximada** de ações para alocar, considerando a alocação percentual e o capital disponível.
             - **Estratégia de Venda:** Se houver recomendações de venda, explique os gatilhos ou condições para realizar a venda.

        **4. PLANEJAMENTO DE LONGO PRAZO E ETAPAS:**
           - Baseado nos objetivos de longo prazo (ex: aposentadoria), crie um **plano de etapas/passos acionáveis** que o usuário deve seguir.
           - Inclua a importância da **diversificação**, **rebalanceamento de carteira** e **reinvestimento de dividendos**.
           - Ofereça **metas anuais ou trimestrais** que ajudem o usuário a monitorar seu progresso.
           - Mencione estratégias para lidar com a inflação e a volatilidade do mercado.

        **Seu Estilo de Relatório (Essencial):**
        - Inicie com um **RESUMO EXECUTIVO** que condensa as principais análises e recomendações.
        - Utilize **cabeçalhos de Markdown (## e ###)** para organizar claramente cada seção (Análise do Perfil, Avaliação de Ativos, Planejamento de Alocação, Planejamento de Longo Prazo, Divulgação de Riscos).
        - Apresente dados financeiros e comparações **exclusivamente em tabelas Markdown**.
        - Use **emojis** (📈📉💰💼⭐📊) para realçar pontos importantes.
        - Destaque **insights chave** e **recomendações específicas** em bullet points.
        - **Explique concisamente qualquer termo técnico** utilizado.
        - Encerre com um **plano de ação claro** e uma **divulgação de riscos** obrigatória.

        **AVISO LEGAL E DIVULGAÇÃO DE RISCOS (OBRIGATÓRIO):**
        - Este relatório é gerado por uma inteligência artificial e destina-se apenas a fins informativos e analíticos. Não constitui aconselhamento financeiro personalizado, legal ou fiscal.
        - Investimentos em renda variável envolvem riscos, incluindo a possível perda do capital investido. Rentabilidade passada não é garantia de rentabilidade futura.
        - As condições de mercado podem mudar rapidamente. Recomenda-se buscar o aconselhamento de um profissional financeiro licenciado e realizar sua própria pesquisa antes de tomar qualquer decisão de investimento.
        - A diversificação é crucial para mitigar riscos.
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
            name="CustomTableText", fontName="Helvetica", fontSize=9, leading=10
        )
    )

    story = []
    lines = text_content.split("\n")
    in_table = False
    table_data = []

    for line in lines:
        stripped_line = line.strip()

        # Lida com tabelas (detecção básica de tabelas Markdown)
        if stripped_line.startswith("|") and "|" in stripped_line[1:]:
            if not in_table:
                in_table = True
                table_data = []
            row = [cell.strip() for cell in stripped_line.split("|") if cell.strip()]
            if row:
                table_data.append(row)
            continue
        elif in_table:  # Fim da tabela (linha vazia ou linha não tabular)
            in_table = False
            if table_data:
                num_cols = len(table_data[0]) if table_data else 0
                if num_cols > 0:
                    table_style = TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
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
                    # Remove a linha separadora de cabeçalho da tabela Markdown
                    if len(table_data) > 1 and all(
                        c.strip().startswith("-") for c in table_data[1]
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
                    story.append(Spacer(1, 0.2 * cm))  #
            table_data = []

        # Lida com cabeçalhos Markdown
        if stripped_line.startswith("## "):
            story.append(Paragraph(stripped_line[3:].strip(), styles["h1"]))
            story.append(Spacer(1, 0.2 * cm))
        elif stripped_line.startswith("### "):
            story.append(Paragraph(stripped_line[4:].strip(), styles["h2"]))
            story.append(Spacer(1, 0.1 * cm))
        # Lida com itens de lista Markdown
        elif stripped_line.startswith("- "):
            story.append(Paragraph(stripped_line, styles["CustomListItem"]))
        # Lida com parágrafos normais e formatação de negrito/itálico
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


# SEU PERFIL DO INVESTIDOR (Formato Markdown otimizado)

meu_perfil_investidor = dedent(
    """
### PERFIL DO INVESTIDOR

**1. Informações Básicas:**
- **Nome:** FULANO
- **Data da Análise:** 2025-07-20

**2. Situação Financeira Atual:**
- **Renda Líquida Mensal:** R$ 3.600,00
- **Gastos Fixos Mensais:** R$ 750,00
- **Economia Mensal Disponível para Investimento:** R$ 2.000,00
- **Reservas Atuais de Emergência:** R$ 3.500,00

**3. Perfil de Risco e Conhecimento:**
- **Tolerância a Risco:** Moderada (Aceito flutuações para ganhos maiores no longo prazo, mas evito riscos excessivos).
- **Nível de Conhecimento em Investimentos:** Intermediário (Compreendo termos básicos e estratégias, mas busco análises aprofundadas).

**4. Objetivos de Investimento:**
- **Curto Prazo (até 1 ano):**
    - **Objetivo:** Atingir R$ 5.000,00 para reserva de emergência.
    - **Prazo Restante:** 6 meses.
    - **Objetivo:** Comparar celular novo ate R$ 4.000
- **Médio Prazo (1 a 5 anos):**
    - **Objetivo:** Adquirir um apartamento no valor de R$ 100.000,00.
    - **Prazo:** 4 anos.
- **Longo Prazo (5+ anos)::**
    - **Objetivo Principal:** Construir patrimônio sólido para aposentadoria, com foco em renda passiva (dividendos e aluguel de fundos imobiliários).
    - **Objetivo Secundário:** Garantir crescimento de capital para cobrir a inflação.

**5. Interesses e Preferências de Investimento:**
- **Ações Atuais de Interesse/Posse:**  GOAU4.SA (GERDAU)(36 reais investidos), MXRF11.SA (Maxi Renda)(996 reais investidos).
- **Setores de Interesse:** Energia, Bancos, Tecnologia, Fundos Imobiliários.
- **Preferência de Renda:** Dividendo (busco empresas com bom histórico e perspectiva de distribuição).
- **Outras Considerações:** Diversificação em renda fixa (Tesouro Direto) para reserva e objetivos de médio prazo.
"""
)

# Prompt para o primeiro agente (Análise Financeira)
prompt_para_analise = dedent(
    f"""\
    Com base no meu PERFIL DO INVESTIDOR abaixo, por favor, gere um relatório de consultoria financeira **MUITO DETALHADO, ABRANGENTE E REALISTA**.
    O relatório deve ser uma análise estratégica aprofundada que cubra todos os pontos solicitados com especificidade e insights práticos.

    Seu relatório deve conter as seguintes seções obrigatórias:

    **1. Análise Aprofundada das Ações de Interesse:**
       - Para cada ação atual (ITUB4.SA, MXRF11.SA):
         - Desempenho recente (últimos 12 meses, 3 anos, 5 anos) e projeções.
         - Análise completa de dividendos (histórico de pagamentos, dividend yield atual, sustentabilidade do dividendo).
         - Recomendações claras (Comprar, Vender, Manter) com justificativas sólidas baseadas em dados fundamentalistas e técnicos.
         - Sugestão precisa de valores ou quantidades para comprar/vender, considerando meu perfil e valor investido.

    **2. Comparativo Setorial e Oportunidades de Migração:**
       - Para cada ação de interesse, identifique **pelo menos 3 a 5 outras empresas líderes do MESMO SETOR** (ex: outros grandes bancos para ITUB4.SA, outras empresas de energia ou siderurgia para GOAU4.SA, outros FIIs para GARE11.SA).
       - Apresente uma **tabela comparativa exaustiva** com métricas financeiras chave (P/L, P/VP, dívida/EBITDA, ROE, crescimento de receita, dividend yield, etc.) e notícias relevantes.
       - Com base nessa comparação e no meu perfil, **avalie EXPLICITAMENTE se compensa migrar** (parcial ou totalmente) ou diversificar para essas empresas alternativas. Forneça os prós e contras específicos de cada ação, e o impacto potencial nos meus objetivos.

    **3. Planejamento de Alocação de Capital Mensal (Curto, Médio e Longo Prazo):**
       - Dada a minha economia mensal disponível (R$ 2.000,00), detalhe um **plano de alocação percentual** para cada um dos meus objetivos:
         - **Curto Prazo:** Como alcançar a reserva de emergência de R$ 5.000,00 e o valor para o celular de R$ 4.000,00, com sugestões de produtos específicos (ex: Tesouro Selic, CDB de liquidez diária) e o tempo estimado.
         - **Médio Prazo:** Como planejar a aquisição do apartamento de R$ 100.000,00 em 4 anos, com alocação em investimentos adequados ao prazo e risco.
         - **Longo Prazo:** Qual a estratégia de alocação para a aposentadoria com foco em renda passiva, detalhando percentuais para ações, FIIs e outras classes de ativos.
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
    {meu_perfil_investidor}
"""
)

print("--- INICIANDO ANÁLISE INICIAL DETALHADA ---")
# Captura a saída completa do primeiro agente
output_lines = []
for chunk in finance_agent.run(prompt_para_analise, stream=True):
    content = getattr(chunk, "content", "")
    if isinstance(content, str) and content.strip():
        output_lines.append(content)

analise_bruta_completa = "".join(output_lines)


print("\n--- INICIANDO REFINAMENTO E FORMATAÇÃO DO RELATÓRIO FINAL ---")
print(analise_bruta_completa)
# Prompt para o segundo agente (Edição/Formatação)
prompt_para_refinamento = dedent(
    f"""\
    Por favor, refine e formate o seguinte rascunho de análise financeira em um relatório único, conciso, profissional e fácil de compreender.
    Certifique-se de que todos os pontos estejam cobertos e inclua a seção de Aviso Legal e Divulgação de Riscos que você conhece.

    RASCUNHO DA ANÁLISE FINANCEIRA:
    {analise_bruta_completa}
"""
)
import time  # Somente se o seu modelo tiver alguma limitação de uso

print("\n--- Aguardando para evitar limite de cota... ---")
time.sleep(60)  # Pausa de 60 segundos antes de chamar o próximo agente


output_lines_final = []
for chunk in report_refiner_agent.run(prompt_para_refinamento, stream=True):
    content = getattr(chunk, "content", "")
    if isinstance(content, str) and content.strip():
        output_lines_final.append(content)


relatorio_final_texto = "".join(output_lines_final)

# --- EXPORTAR PARA PDF ---
if relatorio_final_texto:
    print("\n--- EXPORTANDO RELATÓRIO PARA PDF ---")
    export_to_pdf(relatorio_final_texto, "Relatorio_Financeiro_Personalizado.pdf")
else:
    print("\nNão foi possível gerar o relatório final para exportação em PDF.")

print("\n--- PROCESSO CONCLUÍDO ---")


# print("\n---\n--- ANÁLISE COMPLEMENTAR: Criptomoedas e o Setor Financeiro ---")
# finance_agent.print_response(
#     "Faça uma análise sobre o impacto das criptomoedas nas instituições financeiras tradicionais. "
#     "Mencione empresas do setor financeiro que estão se adaptando ou investindo em blockchain, como JP Morgan (JPM) e Goldman Sachs (GS).",
#     stream=True,
# )
