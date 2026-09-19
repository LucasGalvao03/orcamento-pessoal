import streamlit as st
import pandas as pd

st.set_page_config(page_title="Orçamento - Lucas Galvão", page_icon="💰", layout="wide")

st.title("💰 Orçamento Mensal - Lucas Galvão")

# --- DADOS INICIAIS DA SUA PLANILHA ---
if 'contas' not in st.session_state:
    st.session_state.contas = [
        {"Conta": "BANCO DO BRASIL (CARD)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "BANCO DO BRASIL (CS)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "ITAU (CARD)", "Fatura": 149.67, "Valor Pago": 149.67, "Status": "PAGO", "Data": "30/06/2026"},
        {"Conta": "ITAU (CS)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "SANTANDER (CARD)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "SANTANDER (CS)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "NUBANK (CARD)", "Fatura": 873.03, "Valor Pago": 873.03, "Status": "PAGO", "Data": "30/06/2026"},
        {"Conta": "NUBANK (CS)", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "INVESTIMENTO", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "HONDA CONSORCIO", "Fatura": 659.68, "Valor Pago": 659.68, "Status": "PAGO", "Data": "15/06/2026"},
        {"Conta": "99 PAY (CS)", "Fatura": 955.35, "Valor Pago": 955.35, "Status": "PAGO", "Data": "15/06/2026"},
        {"Conta": "FACULDADE", "Fatura": 201.83, "Valor Pago": 201.83, "Status": "PAGO", "Data": "15/06/2026"},
        {"Conta": "RASTREADOR", "Fatura": 104.90, "Valor Pago": 104.90, "Status": "PAGO", "Data": "22/06/2026"},
        {"Conta": "FINANCIAMENTO CAIXA", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "EMPRESTIMO ITAU", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
        {"Conta": "FINANCIAMENTO IMOBILIARIA", "Fatura": 0.00, "Valor Pago": 0.00, "Status": "ISENTO", "Data": "XX/XX/XXXX"},
    ]

tab_dash, tab_contas, tab_rem, tab_tickets = st.tabs([
    "📈 Resumo & Saldo", "💳 Contas (Editável)", "💵 Remunerações", "🍽️ Tickets"
])

# --- TAB 1: RESUMO ---
with tab_dash:
    st.subheader("📌 Resumo Financeiro Geral")
    df_contas = pd.DataFrame(st.session_state.contas)
    total_pago = df_contas['Valor Pago'].sum()
    
    q1 = st.session_state.get('q1', 1000.00)
    q2 = st.session_state.get('q2', 1500.00)
    he = st.session_state.get('he', 403.86)
    noturno = st.session_state.get('noturno', 137.73)
    dsr_not = st.session_state.get('dsr_not', 27.55)
    dsr_var = st.session_state.get('dsr_var', 80.77)
    
    bruto = q1 + q2 + he + noturno + dsr_not + dsr_var
    inss = st.session_state.get('inss', 266.57)
    ad = st.session_state.get('ad', 1000.00)
    descontos = inss + ad
    liquido = bruto - descontos
    saldo_mes = liquido - total_pago
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Salário Líquido Total", f"R$ {liquido:,.2f}")
    col2.metric("Total Pago em Contas", f"R$ {total_pago:,.2f}")
    col3.metric("Saldo do Mês", f"R$ {saldo_mes:,.2f}")

# --- TAB 2: CONTAS EDITÁVEIS ---
with tab_contas:
    st.subheader("💳 Contas e Faturas")
    st.caption("Você pode adicionar novas linhas, excluir ou alterar valores diretamente na tabela:")
    
    edited_df = st.data_editor(
        pd.DataFrame(st.session_state.contas),
        num_rows="dynamic",
        column_config={
            "Fatura": st.column_config.NumberColumn(format="R$ %.2f"),
            "Valor Pago": st.column_config.NumberColumn(format="R$ %.2f"),
            "Status": st.column_config.SelectboxColumn(options=["PAGO", "PENDENTE", "ISENTO"]),
        },
        use_container_width=True
    )
    st.session_state.contas = edited_df.to_dict('records')

# --- TAB 3: REMUNERAÇÕES ---
with tab_rem:
    c_g, c_d = st.columns(2)
    with c_g:
        st.subheader("Ganhos")
        st.session_state.q1 = st.number_input("Quinzena 1/2", value=st.session_state.get('q1', 1000.00))
        st.session_state.q2 = st.number_input("Quinzena 2/2", value=st.session_state.get('q2', 1500.00))
        st.session_state.he = st.number_input("H.E. 100%", value=st.session_state.get('he', 403.86))
        st.session_state.noturno = st.number_input("Ad. Noturno", value=st.session_state.get('noturno', 137.73))
        st.session_state.dsr_not = st.number_input("DSR Ad. Noturno", value=st.session_state.get('dsr_not', 27.55))
        st.session_state.dsr_var = st.number_input("DSR Variáveis", value=st.session_state.get('dsr_var', 80.77))
    with c_d:
        st.subheader("Descontos")
        st.session_state.inss = st.number_input("INSS", value=st.session_state.get('inss', 266.57))
        st.session_state.ad = st.number_input("Adiantamento", value=st.session_state.get('ad', 1000.00))

# --- TAB 4: TICKETS ---
with tab_tickets:
    c_ta, c_tm = st.columns(2)
    with c_ta:
        st.subheader("Ticket Alimentação/Refeição")
        sal_ant_a = st.number_input("Saldo Anterior (Alim.)", value=17.49)
        sal_at_a = st.number_input("Saldo Atual (Alim.)", value=955.00)
        mateus = st.number_input("Mix Mateus", value=855.00)
        ideal = st.number_input("Ideal", value=117.49)
        outros_a = st.number_input("Outros (Alim.)", value=0.00)
        saldo_f_a = (sal_ant_a + sal_at_a) - (mateus + ideal + outros_a)
        st.metric("Saldo Final Alimentação", f"R$ {saldo_f_a:,.2f}")

    with c_tm:
        st.subheader("Ticket Mobilidade")
        sal_ant_m = st.number_input("Saldo Anterior (Mob.)", value=8.95)
        sal_at_m = st.number_input("Saldo Atual (Mob.)", value=600.00)
        uber = st.number_input("Uber Mensal", value=160.47)
        gas_moto = st.number_input("Gasolina Moto", value=145.18)
        gas_carro = st.number_input("Gasolina Carro", value=300.00)
        saldo_f_m = (sal_ant_m + sal_at_m) - (uber + gas_moto + gas_carro)
        st.metric("Saldo Final Mobilidade", f"R$ {saldo_f_m:,.2f}")
