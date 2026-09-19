import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Configuração da página
st.set_page_config(page_title="Orçamento & Finanças - Lucas Galvão", page_icon="💎", layout="wide")

st.title("💎 Gestão Financeira Inteligente - Lucas Galvão")

# Tentar importar gspread para integração com Google Sheets
try:
    import gspread
    from google.oauth2.service_account import Credentials
    HAS_GSPREAD = True
except ImportError:
    HAS_GSPREAD = False

# --- FUNÇÃO DE CONEXÃO COM GOOGLE SHEETS ---
def obter_cliente_gspread():
    if not HAS_GSPREAD:
        return None
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
            return gspread.authorize(credentials)
    except Exception as e:
        st.sidebar.warning(f"Aviso de conexão Google Sheets: {e}")
    return None

# --- BANCO DE DADOS EM SESSÃO ---
if 'historico_meses' not in st.session_state:
    st.session_state.historico_meses = {
        "Junho / 2026": {
            "contas": [
                {"Conta": "BANCO DO BRASIL (CARD)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/06/2026", "Extrato": "Sem compras no mês"},
                {"Conta": "ITAU (CARD)", "Fatura": 149.67, "Valor Pago": 149.67, "Status": "PAGO", "Data": "30/06/2026", "Extrato": "• Tênis Nike: R$ 99,67 (2/5)\n• Farmácia: R$ 50,00 (1/1)"},
                {"Conta": "NUBANK (CARD)", "Fatura": 873.03, "Valor Pago": 873.03, "Status": "PAGO", "Data": "30/06/2026", "Extrato": "• Mercado Livre: R$ 350,00 (3/10)"},
                {"Conta": "HONDA CONSORCIO", "Fatura": 659.68, "Valor Pago": 659.68, "Status": "PAGO", "Data": "15/06/2026", "Extrato": "• Consórcio Moto (22/60)"},
                {"Conta": "99 PAY (CS)", "Fatura": 955.35, "Valor Pago": 955.35, "Status": "PAGO", "Data": "15/06/2026", "Extrato": "• Transferências"},
                {"Conta": "FACULDADE", "Fatura": 201.83, "Valor Pago": 201.83, "Status": "PAGO", "Data": "15/06/2026", "Extrato": "• Mensalidade (4/12)"},
                {"Conta": "RASTREADOR", "Fatura": 104.90, "Valor Pago": 104.90, "Status": "PAGO", "Data": "22/06/2026", "Extrato": "• Rastreamento Moto"},
            ],
            "rem": {"q1": 1000.0, "q2": 1500.0, "he": 403.86, "not": 137.73, "dsr_not": 27.55, "dsr_var": 80.77, "inss": 266.57, "ad": 1000.0, "emergencia": 0.00},
            "tk": {"sal_a_ant": 17.49, "sal_a_at": 955.0, "mateus": 855.0, "ideal": 117.49, "outros_a": 0.0,
                   "sal_m_ant": 8.95, "sal_m_at": 600.0, "uber": 160.47, "gas_m": 145.18, "gas_c": 300.0}
        },
        "Julho / 2026": {
            "contas": [
                {"Conta": "ITAU (CARD)", "Fatura": 180.66, "Valor Pago": 0.00, "Status": "PAGO", "Data": "31/07/2026", "Extrato": ""},
                {"Conta": "NUBANK (CARD)", "Fatura": 1202.49, "Valor Pago": 0.00, "Status": "PAGO", "Data": "31/07/2026", "Extrato": ""},
                {"Conta": "HONDA CONSORCIO", "Fatura": 659.68, "Valor Pago": 0.00, "Status": "PAGO", "Data": "15/07/2026", "Extrato": ""},
            ],
            "rem": {"q1": 1000.0, "q2": 4068.81, "he": 157.70, "not": 101.03, "dsr_not": 19.43, "dsr_var": 556.98, "inss": 1224.10, "ad": 1000.0, "emergencia": 1055.00},
            "tk": {"sal_a_ant": 0.0, "sal_a_at": 955.0, "mateus": 0.0, "ideal": 0.0, "outros_a": 0.0,
                   "sal_m_ant": 0.0, "sal_m_at": 600.0, "uber": 0.0, "gas_m": 0.0, "gas_c": 0.0}
        },
        "Agosto / 2026": {
            "contas": [
                {"Conta": "ITAU (CARD)", "Fatura": 438.00, "Valor Pago": 0.00, "Status": "PAGO", "Data": "31/08/2026", "Extrato": "• Compras de Agosto"},
                {"Conta": "NUBANK (CARD)", "Fatura": 1211.99, "Valor Pago": 0.00, "Status": "PAGO", "Data": "31/08/2026", "Extrato": "• Fatura do mês"},
                {"Conta": "FACULDADE", "Fatura": 204.83, "Valor Pago": 0.00, "Status": "PAGO", "Data": "15/08/2026", "Extrato": "• Mensalidade (6/12)"},
                {"Conta": "FINANCIAMENTO CAIXA", "Fatura": 450.00, "Valor Pago": 0.00, "Status": "PAGO", "Data": "31/08/2026", "Extrato": "• Habitação (1/360)"},
                {"Conta": "EMPRESTIMO ITAU", "Fatura": 333.00, "Valor Pago": 0.00, "Status": "PAGO", "Data": "31/08/2026", "Extrato": "• Empréstimo (1/24)"},
            ],
            "rem": {"q1": 1025.0, "q2": 1500.0, "he": 252.06, "not": 100.05, "dsr_not": 19.24, "dsr_var": 48.47, "inss": 246.46, "ad": 1025.0, "emergencia": 0.00},
            "tk": {"sal_a_ant": 0.0, "sal_a_at": 955.0, "mateus": 0.0, "ideal": 0.0, "outros_a": 0.0,
                   "sal_m_ant": 0.0, "sal_m_at": 600.0, "uber": 0.0, "gas_m": 0.0, "gas_c": 0.0}
        },
        "Setembro / 2026": {
            "contas": [
                {"Conta": "ITAU (CARD)", "Fatura": 438.56, "Valor Pago": 0.00, "Status": "PENDENTE", "Data": "XX/09/2026", "Extrato": "• Compras Setembro"},
                {"Conta": "NUBANK (CARD)", "Fatura": 771.42, "Valor Pago": 0.00, "Status": "PENDENTE", "Data": "XX/09/2026", "Extrato": "• Fatura em aberto"},
                {"Conta": "FACULDADE", "Fatura": 204.83, "Valor Pago": 0.00, "Status": "PENDENTE", "Data": "XX/09/2026", "Extrato": "• Mensalidade (7/12)"},
                {"Conta": "FINANCIAMENTO CAIXA", "Fatura": 450.00, "Valor Pago": 0.00, "Status": "PENDENTE", "Data": "XX/09/2026", "Extrato": "• Habitação (2/360)"},
                {"Conta": "EMPRESTIMO ITAU", "Fatura": 233.00, "Valor Pago": 0.00, "Status": "PENDENTE", "Data": "XX/09/2026", "Extrato": "• Empréstimo (2/24)"},
            ],
            "rem": {"q1": 1025.0, "q2": 1500.0, "he": 0.0, "not": 0.0, "dsr_not": 0.0, "dsr_var": 0.0, "inss": 0.0, "ad": 1025.0, "emergencia": 0.00},
            "tk": {"sal_a_ant": 0.0, "sal_a_at": 955.0, "mateus": 0.0, "ideal": 0.0, "outros_a": 0.0,
                   "sal_m_ant": 0.0, "sal_m_at": 600.0, "uber": 0.0, "gas_m": 0.0, "gas_c": 0.0}
        }
    }

# --- BARRA LATERAL ---
st.sidebar.header("📅 Navegação do Orçamento")
mes_selecionado = st.sidebar.selectbox("Escolha o Mês:", list(st.session_state.historico_meses.keys()))

novo_mes_nome = st.sidebar.text_input("Adicionar Novo Mês (Ex: Outubro / 2026):")
if st.sidebar.button("➕ Criar Novo Mês"):
    if novo_mes_nome and novo_mes_nome not in st.session_state.historico_meses:
        st.session_state.historico_meses[novo_mes_nome] = {
            "contas": [c.copy() for c in st.session_state.historico_meses[mes_selecionado]["contas"]],
            "rem": st.session_state.historico_meses[mes_selecionado]["rem"].copy(),
            "tk": st.session_state.historico_meses[mes_selecionado]["tk"].copy()
        }
        st.sidebar.success(f"Mês '{novo_mes_nome}' criado com sucesso!")
        st.rerun()

st.caption(f"Exibindo dados referentes a: **{mes_selecionado}**")
dados_mes = st.session_state.historico_meses[mes_selecionado]

# TABS DE NAVEGAÇÃO
tab_dash, tab_contas, tab_rem, tab_tickets, tab_analytics = st.tabs([
    "📈 Dashboard & Saldo", "💳 Gestão de Contas & Extrato", "💵 Remunerações", "🍽️ Tickets & Mobilidade", "📊 Análise Comparativa"
])

# --- DADOS COMPARTILHADOS ---
df_contas = pd.DataFrame(dados_mes["contas"])
total_pago = df_contas['Valor Pago'].sum() if 'Valor Pago' in df_contas.columns else 0.0
total_faturas = df_contas['Fatura'].sum() if 'Fatura' in df_contas.columns else 0.0

rem = dados_mes["rem"]
salario_bruto = rem["q1"] + rem["q2"] + rem["he"] + rem["not"] + rem["dsr_not"] + rem["dsr_var"]
descontos = rem["inss"] + rem["ad"]
salario_liquido = salario_bruto - descontos
valor_emergencia = rem.get("emergencia", 0.00)

saldo_mes = salario_liquido - (total_pago if total_pago > 0 else total_faturas)
taxa_comprometimento = (total_faturas / salario_liquido * 100) if salario_liquido > 0 else 0

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.subheader(f"⚡ Resumo Executivo - {mes_selecionado}")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Salário Líquido", f"R$ {salario_liquido:,.2f}")
    c2.metric("Total Faturado", f"R$ {total_faturas:,.2f}")
    c3.metric("Saldo do Mês", f"R$ {saldo_mes:,.2f}", delta=f"{'-' if saldo_mes < 0 else '+'}{abs(saldo_mes):,.2f}")
    c4.metric("🚨 Emergência", f"R$ {valor_emergencia:,.2f}")
    
    tk = dados_mes["tk"]
    tk_alim_saldo = (tk["sal_a_ant"] + tk["sal_a_at"]) - (tk["mateus"] + tk["ideal"] + tk["outros_a"])
    tk_mob_saldo = (tk["sal_m_ant"] + tk["sal_m_at"]) - (tk["uber"] + tk["gas_m"] + tk["gas_c"])
    
    recursos_totais = salario_liquido + tk_alim_saldo + tk_mob_saldo + valor_emergencia
    c5.metric("Recursos Totais (+ Emergência)", f"R$ {recursos_totais:,.2f}")

    st.divider()

    st.markdown("### 🚦 Saúde Financeira do Mês")
    if taxa_comprometimento > 85:
        st.error(f"⚠️ **Atenção:** Despesas comprometendo **{taxa_comprometimento:.1f}%** da renda do mês!")
    elif taxa_comprometimento > 70:
        st.warning(f"⚡ **Aviso:** Comprometimento em **{taxa_comprometimento:.1f}%**.")
    else:
        st.success(f"✅ **Excelente!** Comprometimento controlado em **{taxa_comprometimento:.1f}%**.")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**Status das Contas**")
        status_counts = df_contas['Status'].value_counts().reset_index() if 'Status' in df_contas.columns else pd.DataFrame()
        if not status_counts.empty:
            fig_status = px.pie(status_counts, values='count', names='Status', hole=0.5)
            st.plotly_chart(fig_status, width="stretch")

    with col_g2:
        st.markdown("**Balanço do Mês**")
        df_balanco = pd.DataFrame({
            "Categoria": ["Salário Líquido", "Total Faturas", "Saldo Restante", "Reserva Emergência"],
            "Valor": [salario_liquido, total_faturas, max(saldo_mes, 0), valor_emergencia]
        })
        fig_bar = px.bar(df_balanco, x="Categoria", y="Valor", text_auto='.2f', color="Categoria")
        st.plotly_chart(fig_bar, width="stretch")

# --- TAB 2: CONTAS ---
with tab_contas:
    st.subheader(f"💳 Tabela de Faturas - {mes_selecionado}")
    
    def salvar_alteracoes_tabela():
        key = f"editor_v7_{mes_selecionado}"
        if key in st.session_state:
            mudancas = st.session_state[key]
            for idx_str, cols in mudancas.get("edited_rows", {}).items():
                idx = int(idx_str)
                for col_name, val in cols.items():
                    st.session_state.historico_meses[mes_selecionado]["contas"][idx][col_name] = val

    df_editor = pd.DataFrame(st.session_state.historico_meses[mes_selecionado]["contas"])
    
    edited_df = st.data_editor(
        df_editor,
        num_rows="dynamic",
        column_config={
            "Conta": st.column_config.TextColumn("Conta / Banco"),
            "Fatura": st.column_config.NumberColumn("Fatura (R$)", format="R$ %.2f"),
            "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f"),
            "Status": st.column_config.SelectboxColumn("Status", options=["PAGO", "PENDENTE", "ISENTO"]),
            "Data": st.column_config.TextColumn("Vencimento / Data"),
            "Extrato": None
        },
        width="stretch",
        key=f"editor_v7_{mes_selecionado}",
        on_change=salvar_alteracoes_tabela
    )

    st.markdown(f"**Total Mês Faturado:** `R$ {edited_df['Fatura'].sum():,.2f}` | **Total Efectivamente Pago:** `R$ {edited_df['Valor Pago'].sum():,.2f}`")

# --- TAB 3: REMUNERAÇÕES ---
with tab_rem:
    st.subheader(f"💵 Folha de Pagamento & Emergência - {mes_selecionado}")
    col_g, col_d = st.columns(2)
    
    with col_g:
        st.markdown("#### 📥 Ganhos")
        rem["q1"] = st.number_input("Quinzena 1/2", value=float(rem["q1"]), key=f"q1_{mes_selecionado}")
        rem["q2"] = st.number_input("Quinzena 2/2", value=float(rem["q2"]), key=f"q2_{mes_selecionado}")
        rem["he"] = st.number_input("Horas Extras 100%", value=float(rem["he"]), key=f"he_{mes_selecionado}")
        rem["not"] = st.number_input("Adicional Noturno", value=float(rem["not"]), key=f"not_{mes_selecionado}")
        rem["dsr_not"] = st.number_input("DSR Adicional Noturno", value=float(rem["dsr_not"]), key=f"dsr_not_{mes_selecionado}")
        rem["dsr_var"] = st.number_input("DSR Variáveis", value=float(rem["dsr_var"]), key=f"dsr_var_{mes_selecionado}")
        st.info(f"**Salário Bruto:** R$ {salario_bruto:,.2f}")

    with col_d:
        st.markdown("#### 📤 Descontos & Reserva de Emergência")
        rem["inss"] = st.number_input("INSS", value=float(rem["inss"]), key=f"inss_{mes_selecionado}")
        rem["ad"] = st.number_input("Adiantamento", value=float(rem["ad"]), key=f"ad_{mes_selecionado}")
        st.error(f"**Total Descontos:** R$ {descontos:,.2f}")
        st.success(f"**Salário Líquido:** R$ {salario_liquido:,.2f}")
        
        st.divider()
        st.markdown("#### 🚨 Reserva de Emergência do Mês")
        rem["emergencia"] = st.number_input("Saldo de Emergência (R$)", value=float(rem.get("emergencia", 0.00)), key=f"emg_{mes_selecionado}")

# --- TAB 4: TICKETS ---
with tab_tickets:
    st.subheader(f"🎟️ Benefícios - {mes_selecionado}")
    c_ta, c_tm = st.columns(2)
    
    with c_ta:
        st.markdown("### 🍽️ Alimentação")
        tk["sal_a_ant"] = st.number_input("Saldo Anterior", value=float(tk["sal_a_ant"]), key=f"sa_ant_{mes_selecionado}")
        tk["sal_a_at"] = st.number_input("Crédito Mês", value=float(tk["sal_a_at"]), key=f"sa_at_{mes_selecionado}")
        tk["mateus"] = st.number_input("Mix Mateus", value=float(tk["mateus"]), key=f"mat_{mes_selecionado}")
        tk["ideal"] = st.number_input("Ideal", value=float(tk["ideal"]), key=f"id_{mes_selecionado}")
        tk["outros_a"] = st.number_input("Outros", value=float(tk["outros_a"]), key=f"out_a_{mes_selecionado}")
        st.metric("Saldo Restante (Alimentação)", f"R$ {tk_alim_saldo:,.2f}")

    with c_tm:
        st.markdown("### 🚌 Mobilidade")
        tk["sal_m_ant"] = st.number_input("Saldo Anterior", value=float(tk["sal_m_ant"]), key=f"sm_ant_{mes_selecionado}")
        tk["sal_m_at"] = st.number_input("Crédito Mês", value=float(tk["sal_m_at"]), key=f"sm_at_{mes_selecionado}")
        tk["uber"] = st.number_input("Uber", value=float(tk["uber"]), key=f"ub_{mes_selecionado}")
        tk["gas_m"] = st.number_input("Gasolina Moto", value=float(tk["gas_m"]), key=f"gm_{mes_selecionado}")
        tk["gas_c"] = st.number_input("Gasolina Carro", value=float(tk["gas_c"]), key=f"gc_{mes_selecionado}")
        st.metric("Saldo Restante (Mobilidade)", f"R$ {tk_mob_saldo:,.2f}")

# --- TAB 5: COMPARAÇÃO ---
with tab_analytics:
    st.subheader("📊 Comparativo Histórico entre Meses")
    
    resumo_historico = []
    for m, d in st.session_state.historico_meses.items():
        df_temp = pd.DataFrame(d["contas"])
        r_temp = d["rem"]
        sb = r_temp["q1"] + r_temp["q2"] + r_temp["he"] + r_temp["not"] + r_temp["dsr_not"] + r_temp["dsr_var"]
        sl = sb - (r_temp["inss"] + r_temp["ad"])
        resumo_historico.append({
            "Mês": m,
            "Salário Líquido": sl,
            "Total Faturas": df_temp['Fatura'].sum() if 'Fatura' in df_temp.columns else 0.0,
            "Emergência": r_temp.get("emergencia", 0.00)
        })
    
    df_hist = pd.DataFrame(resumo_historico)
    fig_comp = px.bar(df_hist, x="Mês", y=["Salário Líquido", "Total Faturas", "Emergência"], barmode="group")
    st.plotly_chart(fig_comp, width="stretch")
