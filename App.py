import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Orçamento & Finanças - Lucas Galvão", page_icon="💎", layout="wide")

st.title("💎 Gestão Financeira Inteligente - Lucas Galvão")

# --- BANCO DE DADOS DE MESES ---
if 'historico_meses' not in st.session_state:
    st.session_state.historico_meses = {
        "Junho / 2026": {
            "contas": [
                {"Conta": "BANCO DO BRASIL (CARD)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/06/2026", "Extrato": "Sem movimentação"},
                {"Conta": "ITAU (CARD)", "Fatura": 149.67, "Valor Pago": 149.67, "Status": "PAGO", "Data": "30/06/2026", "Extrato": "• Tênis Nike: R$ 99,67 (2/5)\n• Farmácia Drogasil: R$ 50,00 (1/1)"},
                {"Conta": "NUBANK (CARD)", "Fatura": 873.03, "Valor Pago": 873.03, "Status": "PAGO", "Data": "30/06/2026", "Extrato": "• Mercado Livre: R$ 350,00 (3/10)\n• Roupas C&A: R$ 200,00 (1/2)\n• Assinaturas/Streamings: R$ 323,03"},
                {"Conta": "HONDA CONSORCIO", "Fatura": 659.68, "Valor Pago": 659.68, "Status": "PAGO", "Data": "15/06/2026", "Extrato": "• Parcela Consórcio Moto (24/60)"},
                {"Conta": "99 PAY (CS)", "Fatura": 955.35, "Valor Pago": 955.35, "Status": "PAGO", "Data": "15/06/2026", "Extrato": "• Pagamento de boletos e transferências da quinzena"},
                {"Conta": "FACULDADE", "Fatura": 201.83, "Valor Pago": 201.83, "Status": "PAGO", "Data": "15/06/2026", "Extrato": "• Mensalidade Curso (6/12)"},
                {"Conta": "RASTREADOR", "Fatura": 104.90, "Valor Pago": 104.90, "Status": "PAGO", "Data": "22/06/2026", "Extrato": "• Mensalidade Rastreamento Veicular Moto"},
            ],
            "rem": {"q1": 1000.0, "q2": 1500.0, "he": 403.86, "not": 137.73, "dsr_not": 27.55, "dsr_var": 80.77, "inss": 266.57, "ad": 1000.0},
            "tk": {"sal_a_ant": 17.49, "sal_a_at": 955.0, "mateus": 855.0, "ideal": 117.49, "outros_a": 0.0,
                   "sal_m_ant": 8.95, "sal_m_at": 600.0, "uber": 160.47, "gas_m": 145.18, "gas_c": 300.0}
        }
    }

# --- SELEÇÃO DE MÊS NA SIDEBAR ---
st.sidebar.header("📅 Navegação do Orçamento")
mes_selecionado = st.sidebar.selectbox("Escolha o Mês:", list(st.session_state.historico_meses.keys()))
dados_mes = st.session_state.historico_meses[mes_selecionado]

tab_dash, tab_contas, tab_rem, tab_tickets = st.tabs([
    "📈 Dashboard & Saldo", "💳 Gestão de Contas & Extrato", "💵 Remunerações", "🍽️ Tickets"
])

# --- TAB 2: GESTÃO DE CONTAS COM EXTRATOS SUSPENSOS ---
with tab_contas:
    st.subheader(f"💳 Tabela de Faturas - {mes_selecionado}")
    
    # 1. TABELA PRINCIPAL LIMPA
    df_contas = pd.DataFrame(dados_mes["contas"])
    
    edited_df = st.data_editor(
        df_contas,
        num_rows="dynamic",
        column_config={
            "Conta": st.column_config.TextColumn("Conta / Banco"),
            "Fatura": st.column_config.NumberColumn("Fatura (R$)", format="R$ %.2f"),
            "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f"),
            "Status": st.column_config.SelectboxColumn("Status", options=["PAGO", "PENDENTE", "ISENTO"]),
            "Data": st.column_config.TextColumn("Vencimento"),
            "Extrato": None # Oculta a coluna de texto longo da tabela para mantê-la limpa
        },
        use_container_width=True,
        key=f"editor_limpo_{mes_selecionado}"
    )
    dados_mes["contas"] = edited_df.to_dict('records')

    st.markdown(f"**Total Mês Faturado:** `R$ {edited_df['Fatura'].sum():,.2f}` | **Total Efectivamente Pago:** `R$ {edited_df['Valor Pago'].sum():,.2f}`")

    st.divider()

    # 2. SEÇÃO DE EXTRATOS E DESCRIMINAÇÃO MANUAI (EXPANDER SUSPENSO)
    st.subheader("🔍 Discriminação & Extrato Detalhado da Conta")
    st.caption("Selecione uma conta abaixo para visualizar ou preencher manualmente o extrato de compras e parcelas:")

    contas_lista = [c["Conta"] for c in dados_mes["contas"]]
    conta_escolhida = st.selectbox("Escolha a Conta para ver/editar o extrato:", contas_lista)

    # Localiza os dados da conta selecionada
    for item in dados_mes["contas"]:
        if item["Conta"] == conta_escolhida:
            with st.expander(f"📄 Extrato Suspenso: {conta_escolhida}", expanded=True):
                # Campo de texto multilinha para colar ou digitar o extrato
                novo_extrato = st.text_area(
                    "Discriminação dos Gastos / Parcelas (Edição Manual):",
                    value=item.get("Extrato", ""),
                    height=150,
                    key=f"txt_{conta_escolhida}_{mes_selecionado}"
                )
                item["Extrato"] = novo_extrato
                st.success("Extrato atualizado e salvo automaticamente!")
