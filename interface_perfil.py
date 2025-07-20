import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime


def run_profile_app():
    """
    Cria e executa a interface gráfica para coletar os dados do perfil do investidor.
    Retorna um dicionário com os dados coletados ou None se a janela for fechada.
    """
    profile_data = {}

    def submit_profile():
        nonlocal profile_data
        try:
            profile_data = {
                "nome": entry_nome.get().strip(),
                "renda_mensal": float(entry_renda.get().replace(",", ".").strip()),
                "gastos_fixos": float(entry_gastos.get().replace(",", ".").strip()),
                "reservas_emergencia": float(
                    entry_reservas.get().replace(",", ".").strip()
                ),
                "tolerancia_risco": var_tolerancia_risco.get(),
                "nivel_conhecimento": var_nivel_conhecimento.get(),
                "obj_curto": entry_obj_curto.get().strip(),
                "prazo_curto_meses": entry_prazo_curto_meses.get().strip(),
                "obj_medio": entry_obj_medio.get().strip(),
                "prazo_medio_anos": entry_prazo_medio_anos.get().strip(),
                "obj_longo": entry_obj_longo.get().strip(),
                "acoes_interesse": entry_acoes_interesse.get(
                    "1.0", tk.END
                ).strip(), 
                "setores_interesse": entry_setores_interesse.get().strip(),
                "pref_renda": var_pref_renda.get(),
                "outras_consideracoes": entry_outras_consideracoes.get(
                    "1.0", tk.END
                ).strip(), 
            }

            if not profile_data["nome"]:
                messagebox.showerror("Erro", "O campo 'Nome' é obrigatório.")
                return
            if not all(
                isinstance(profile_data[k], (int, float))
                for k in ["renda_mensal", "gastos_fixos", "reservas_emergencia"]
            ):
                messagebox.showerror(
                    "Erro", "Valores monetários devem ser números válidos."
                )
                return
            if not profile_data["obj_longo"]:
                messagebox.showerror(
                    "Erro", "O campo 'Objetivo Principal (Longo Prazo)' é obrigatório."
                )
                return

            root.destroy()  
        except ValueError:
            messagebox.showerror(
                "Erro de Entrada",
                "Por favor, insira números válidos para os campos monetários e prazos.",
            )
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    root = tk.Tk()
    root.title("Perfil do Investidor")
    root.geometry("900x850")  
    root.resizable(False, False)
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    second_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Estilos
    label_font = ("Helvetica", 10, "bold")
    entry_font = ("Helvetica", 10)
    section_font = ("Helvetica", 12, "bold")

    row_idx = 0

    # Seção 1: Informações Básicas
    tk.Label(second_frame, text="1. Informações Básicas", font=section_font).grid(
        row=row_idx, column=0, columnspan=2, pady=10, sticky="w"
    )
    row_idx += 1
    tk.Label(second_frame, text="Nome:", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    entry_nome = tk.Entry(second_frame, width=50, font=entry_font)
    entry_nome.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    row_idx += 1

    # Seção 2: Situação Financeira Atual
    tk.Label(second_frame, text="2. Situação Financeira Atual", font=section_font).grid(
        row=row_idx, column=0, columnspan=2, pady=10, sticky="w"
    )
    row_idx += 1
    tk.Label(second_frame, text="Renda Líquida Mensal (R$):", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    entry_renda = tk.Entry(second_frame, width=50, font=entry_font)
    entry_renda.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_renda.insert(0, "0.00")
    row_idx += 1
    tk.Label(second_frame, text="Gastos Fixos Mensais (R$):", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    entry_gastos = tk.Entry(second_frame, width=50, font=entry_font)
    entry_gastos.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_gastos.insert(0, "0.00")
    row_idx += 1
    tk.Label(
        second_frame, text="Reservas Atuais de Emergência (R$):", font=label_font
    ).grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
    entry_reservas = tk.Entry(second_frame, width=50, font=entry_font)
    entry_reservas.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_reservas.insert(0, "0.00")
    row_idx += 1

    # Seção 3: Perfil de Risco e Conhecimento
    tk.Label(
        second_frame, text="3. Perfil de Risco e Conhecimento", font=section_font
    ).grid(row=row_idx, column=0, columnspan=2, pady=10, sticky="w")
    row_idx += 1
    tk.Label(second_frame, text="Tolerância a Risco:", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    var_tolerancia_risco = tk.StringVar(root)
    var_tolerancia_risco.set("Moderada")  # default value
    opcoes_risco = ["Conservadora", "Moderada", "Agressiva"]
    option_menu_risco = tk.OptionMenu(second_frame, var_tolerancia_risco, *opcoes_risco)
    option_menu_risco.config(width=47, font=entry_font)
    option_menu_risco.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    row_idx += 1

    tk.Label(second_frame, text="Nível de Conhecimento:", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    var_nivel_conhecimento = tk.StringVar(root)
    var_nivel_conhecimento.set("Intermediário")  # default value
    opcoes_conhecimento = ["Iniciante", "Intermediário", "Avançado", "Especialista"]
    option_menu_conhecimento = tk.OptionMenu(
        second_frame, var_nivel_conhecimento, *opcoes_conhecimento
    )
    option_menu_conhecimento.config(width=47, font=entry_font)
    option_menu_conhecimento.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    row_idx += 1

    # Seção 4: Objetivos de Investimento
    tk.Label(second_frame, text="4. Objetivos de Investimento", font=section_font).grid(
        row=row_idx, column=0, columnspan=2, pady=10, sticky="w"
    )
    row_idx += 1
    tk.Label(second_frame, text="Curto Prazo (até 1 ano):", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    entry_obj_curto = tk.Entry(second_frame, width=50, font=entry_font)
    entry_obj_curto.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_obj_curto.insert(0, "Atingir R$ 5.000,00 para reserva de emergência.")
    row_idx += 1
    tk.Label(second_frame, text="Prazo Restante (meses):", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    entry_prazo_curto_meses = tk.Entry(second_frame, width=50, font=entry_font)
    entry_prazo_curto_meses.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_prazo_curto_meses.insert(0, "6")
    row_idx += 1

    tk.Label(second_frame, text="Médio Prazo (1 a 5 anos):", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    entry_obj_medio = tk.Entry(second_frame, width=50, font=entry_font)
    entry_obj_medio.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_obj_medio.insert(0, "Adquirir um apartamento no valor de R$ 100.000,00.")
    row_idx += 1
    tk.Label(second_frame, text="Prazo (anos):", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    entry_prazo_medio_anos = tk.Entry(second_frame, width=50, font=entry_font)
    entry_prazo_medio_anos.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_prazo_medio_anos.insert(0, "4")
    row_idx += 1

    tk.Label(
        second_frame, text="Longo Prazo (5+ anos - Principal):", font=label_font
    ).grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
    entry_obj_longo = tk.Entry(second_frame, width=50, font=entry_font)
    entry_obj_longo.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_obj_longo.insert(
        0,
        "Construir patrimônio sólido para aposentadoria, com foco em renda passiva (dividendos e aluguel de fundos imobiliários).",
    )
    row_idx += 1

    # Seção 5: Interesses e Preferências de Investimento
    tk.Label(
        second_frame,
        text="5. Interesses e Preferências de Investimento",
        font=section_font,
    ).grid(row=row_idx, column=0, columnspan=2, pady=10, sticky="w")
    row_idx += 1
    tk.Label(
        second_frame,
        text="Ações de Interesse/Posse Adicione o '.SA' ):",
        font=label_font,
    ).grid(row=row_idx, column=0, sticky="nw", padx=5, pady=2)
    entry_acoes_interesse = scrolledtext.ScrolledText(
        second_frame, width=50, height=3, font=entry_font, wrap=tk.WORD
    )
    entry_acoes_interesse.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_acoes_interesse.insert(
        tk.END, "GOAU4.SA (36 reais investidos) Adicione o '.SA'"
    )
    row_idx += 1

    tk.Label(
        second_frame,
        text="Setores de Interesse (Ex: Energia, Bancos):",
        font=label_font,
    ).grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
    entry_setores_interesse = tk.Entry(second_frame, width=50, font=entry_font)
    entry_setores_interesse.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_setores_interesse.insert(
        0, "Energia, Bancos, Tecnologia, Fundos Imobiliários"
    )
    row_idx += 1

    tk.Label(second_frame, text="Preferência de Renda:", font=label_font).grid(
        row=row_idx, column=0, sticky="w", padx=5, pady=2
    )
    var_pref_renda = tk.StringVar(root)
    var_pref_renda.set("Dividendo")  # default value
    opcoes_renda = ["Crescimento de Capital", "Dividendo", "Ambos"]
    option_menu_renda = tk.OptionMenu(second_frame, var_pref_renda, *opcoes_renda)
    option_menu_renda.config(width=47, font=entry_font)
    option_menu_renda.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    row_idx += 1

    tk.Label(second_frame, text="Outras Considerações:", font=label_font).grid(
        row=row_idx, column=0, sticky="nw", padx=5, pady=2
    )
    entry_outras_consideracoes = scrolledtext.ScrolledText(
        second_frame, width=50, height=3, font=entry_font, wrap=tk.WORD
    )
    entry_outras_consideracoes.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
    entry_outras_consideracoes.insert(
        tk.END,
        "Diversificação em renda fixa (Tesouro Direto) para reserva e objetivos de médio prazo.",
    )
    row_idx += 1

    # Botão de Submissão
    submit_button = tk.Button(
        second_frame,
        text="Gerar Relatório Financeiro",
        command=submit_profile,
        font=label_font,
        bg="#4CAF50",
        fg="white",
    )
    submit_button.grid(row=row_idx, column=0, columnspan=2, pady=20)

    second_frame.grid_columnconfigure(1, weight=1)

    root.protocol(
        "WM_DELETE_WINDOW", lambda: root.destroy()
    )  

    root.mainloop()
    return profile_data


if __name__ == "__main__":
    dados = run_profile_app()
    if dados:
        print("Dados do perfil coletados:")
        for key, value in dados.items():
            print(f"- {key}: {value}")
    else:
        print("Nenhum dado coletado. Janela fechada.")
