import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Orçamento & Finanças - Lucas Galvão", page_icon="💎", layout="wide")

st.title("💎 Gestão Financeira Inteligente - Lucas Galvão")
st.caption("Painel executivo de controle de orçamento, benefícios e projeção de caixa.")

# --- INICIALIZAÇÃO DE DADOS (SESSÃO) ---
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

# TABS NAVEGAÇÃO
tab_dash, tab_contas, tab_rem, tab_tickets, tab_analytics = st.tabs([
    "📈 Dashboard & Saldo", "💳 Gestão de Contas", "💵 Remunerações", "🍽️ Tickets & Mobilidade", "📊 Análise Avançada"
])

# --- DADOS COMPARTILHADOS ---
df_contas = pd.DataFrame(st.session_state.contas)
total_pago = df_contas['Valor Pago'].sum()
total_faturas = df_contas['Fatura'].sum()

q1 = st.session_state.get('q1', 1000.00)
q2 = st.session_state.get('q2', 1500.00)
he = st.session_state.get('he', 403.86)
noturno = st.session_state.get('noturno', 137.73)
dsr_not = st.session_state.get('dsr_not', 27.55)
dsr_var = st.session_state.get('dsr_var', 80.77)

salario_bruto = q1 + q2 + he + noturno + dsr_not + dsr_var
inss = st.session_state.get('inss', 266.57)
ad = st.session_state.get('ad', 1000.00)
descontos = inss + ad
salario_liquido = salario_bruto - descontos

saldo_mes = salario_liquido - total_pago
taxa_comprometimento = (total_pago / salario_liquido * 100) if salario_liquido > 0 else 0

# --- TAB 1: DASHBOARD PRINCIPAL ---
with tab_dash:
    st.subheader("⚡ Resumo Financeiro Executivo")
    
    # KPIs Topo
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Salário Líquido", f"R$ {salario_liquido:,.2f}")
    c2.metric("Total de Contas Pagas", f"R$ {total_pago:,.2f}")
    
    # Cor condicional do Saldo
    delta_text = f"Comprometimento: {taxa_comprometimento:.1f}%"
    c3.metric("Saldo Líquido Livre", f"R$ {saldo_mes:,.2f}", delta=f"{'-' if saldo_mes < 0 else '+'}{abs(saldo_mes):,.2f}")
    
    # Benefícios Globais
    tk_alim_saldo = st.session_state.get('tk_alim_saldo', 0.00)
    tk_mob_saldo = st.session_state.get('tk_mob_saldo', 3.30)
    patrimonio_mes = salario_liquido + tk_alim_saldo + tk_mob_saldo
    c4.metric("Recursos Totais (Salário + Tickets)", f"R$ {patrimonio_mes:,.2f}")

    st.divider()

    # Indicadores da Saude Financeira
    st.markdown("### 🚦 Saúde Financeira do Mês")
    if taxa_comprometimento > 85:
        st.error(f"⚠️ **Atenção:** Suas despesas estão comprometendo **{taxa_comprometimento:.1f}%** da sua renda. Margem de segurança baixa!")
    elif taxa_comprometimento > 70:
        st.warning(f"⚡ **Aviso:** Comprometimento em **{taxa_comprometimento:.1f}%**. Ideal manter abaixo de 70%.")
    else:
        st.success(f"✅ **Excelente!** Comprometimento controlado em **{taxa_comprometimento:.1f}%**. Sobra disponível para reserva/investimentos.")

    # Gráfico Rápido
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**Status das Contas**")
        status_counts = df_contas['Status'].value_counts().reset_index()
        fig_status = px.pie(status_counts, values='count', names='Status', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_status, use_container_width=True)

    with col_g2:
        st.markdown("**Balanço de Caixa (Ganhos vs Saídas)**")
        df_balanco = pd.DataFrame({
            "Categoria": ["Salário Líquido", "Despesas Pagas", "Saldo Restante"],
            "Valor": [salario_liquido, total_pago, max(saldo_mes, 0)]
        })
        fig_bar = px.bar(df_balanco, x="Categoria", y="Valor", text_auto='.2f', color="Categoria", color_discrete_sequence=['#2ecc71', '#e74c3c', '#3498db'])
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 2: GESTÃO DE CONTAS ---
with tab_contas:
    st.subheader("💳 Gestão Interativa de Faturas e Despesas")
    st.caption("Edite valores, adicione ou remova parcelas em tempo real:")
    
    edited_df = st.data_editor(
        pd.DataFrame(st.session_state.contas),
        num_rows="dynamic",
        column_config={
            "Fatura": st.column_config.NumberColumn("Fatura (R$)", format="R$ %.2f"),
            "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f"),
            "Status": st.column_config.SelectboxColumn("Status", options=["PAGO", "PENDENTE", "ISENTO"]),
            "Data": st.column_config.TextColumn("Vencimento / Data")
        },
        use_container_width=True,
        key="editor_contas_v2"
    )
    st.session_state.contas = edited_df.to_dict('records')
    
    col_exp1, col_exp2 = st.columns([3, 1])
    with col_exp1:
        st.markdown(f"**Total Mês Faturado:** `R$ {edited_df['Fatura'].sum():,.2f}` | **Total Efectivamente Pago:** `R$ {edited_df['Valor Pago'].sum():,.2f}`")
    with col_exp2:
        # Download de Relatório CSV
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Relatório (CSV)", csv, "orcamento_lucas.csv", "text/csv")

# --- TAB 3: REMUNERAÇÕES ---
with tab_rem:
    st.subheader("💵 Detalhamento da Folha de Pagamento")
    col_g, col_d = st.columns(2)
    
    with col_g:
        st.markdown("#### 📥 Ganhos & Adicionais")
        st.session_state.q1 = st.number_input("Quinzena 1/2", value=st.session_state.get('q1', 1000.00), step=50.0)
        st.session_state.q2 = st.number_input("Quinzena 2/2", value=st.session_state.get('q2', 1500.00), step=50.0)
        st.session_state.he = st.number_input("Horas Extras (100%)", value=st.session_state.get('he', 403.86), step=10.0)
        st.session_state.noturno = st.number_input("Adicional Noturno", value=st.session_state.get('noturno', 137.73), step=10.0)
        st.session_state.dsr_not = st.number_input("DSR Adicional Noturno", value=st.session_state.get('dsr_not', 27.55), step=5.0)
        st.session_state.dsr_var = st.number_input("DSR Variáveis", value=st.session_state.get('dsr_var', 80.77), step=5.0)
        
        st.info(f"**Salário Bruto Total:** R$ {salario_bruto:,.2f}")

    with col_d:
        st.markdown("#### 📤 Descontos de Lei & Quinzena")
        st.session_state.inss = st.number_input("Desconto INSS", value=st.session_state.get('inss', 266.57), step=10.0)
        st.session_state.ad = st.number_input("Adiantamento (Dia 15)", value=st.session_state.get('ad', 1000.00), step=50.0)
        
        st.error(f"**Total de Descontos:** R$ {descontos:,.2f}")
        st.success(f"**Salário Líquido em Conta:** R$ {salario_liquido:,.2f}")

# --- TAB 4: TICKETS & MOBILIDADE ---
with tab_tickets:
    st.subheader("🎟️ Gestão Inteligente de Benefícios")
    
    c_ta, c_tm = st.columns(2)
    
    with c_ta:
        st.markdown("### 🍽️ Ticket Alimentação / Refeição")
        sal_ant_a = st.number_input("Saldo Anterior (Alim.)", value=17.49)
        sal_at_a = st.number_input("Crédito do Mês (Alim.)", value=955.00)
        tk_alim_real = sal_ant_a + sal_at_a
        st.caption(f"Total Disponível: **R$ {tk_alim_real:,.2f}**")
        
        st.markdown("**Extrato de Compras:**")
        mateus = st.number_input("Mix Mateus", value=855.00)
        ideal = st.number_input("Ideal", value=117.49)
        outros_a = st.number_input("Outros Supermercados", value=0.00)
        
        gasto_alim = mateus + ideal + outros_a
        st.session_state.tk_alim_saldo = tk_alim_real - gasto_alim
        
        # Barra de consumo do benefício
        pct_alim = min(gasto_alim / tk_alim_real, 1.0) if tk_alim_real > 0 else 0
        st.progress(pct_alim, text=f"Consumido: {pct_alim*100:.1f}% do saldo")
        st.metric("Saldo Restante (Alimentação)", f"R$ {st.session_state.tk_alim_saldo:,.2f}")

    with c_tm:
        st.markdown("### 🚌 Ticket Mobilidade & Combustível")
        sal_ant_m = st.number_input("Saldo Anterior (Mob.)", value=8.95)
        sal_at_m = st.number_input("Crédito do Mês (Mob.)", value=600.00)
        tk_mob_real = sal_ant_m + sal_at_m
        st.caption(f"Total Disponível: **R$ {tk_mob_real:,.2f}**")
        
        st.markdown("**Extrato de Mobilidade:**")
        uber = st.number_input("Uber / App", value=160.47)
        gas_moto = st.number_input("Gasolina Moto", value=145.18)
        gas_carro = st.number_input("Gasolina Carro", value=300.00)
        
        gasto_mob = uber + gas_moto + gas_carro
        st.session_state.tk_mob_saldo = tk_mob_real - gasto_mob
        
        # Barra de consumo do benefício
        pct_mob = min(gasto_mob / tk_mob_real, 1.0) if tk_mob_real > 0 else 0
        st.progress(pct_mob, text=f"Consumido: {pct_mob*100:.1f}% do saldo")
        st.metric("Saldo Restante (Mobilidade)", f"R$ {st.session_state.tk_mob_saldo:,.2f}")

# --- TAB 5: ANÁLISE AVANÇADA ---
with tab_analytics:
    st.subheader("📊 Análise de Custos de Mobilidade & Perfil de Consumo")
    
    col_an1, col_an2 = st.columns(2)
    
    with col_an1:
        st.markdown("#### ⛽ Divisão dos Custos de Transporte")
        df_mob = pd.DataFrame({
            "Categoria": ["Uber", "Gasolina Moto", "Gasolina Carro"],
            "Valor": [uber, gas_moto, gas_carro]
        })
        fig_mob = px.pie(df_mob, values='Valor', names='Categoria', color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_mob, use_container_width=True)
        
    with col_an2:
        st.markdown("#### 🛒 Composição dos Gastos de Alimentação")
        df_alim = pd.DataFrame({
            "Estabelecimento": ["Mix Mateus", "Ideal", "Outros"],
            "Valor": [mateus, ideal, outros_a]
        })
        fig_alim = px.bar(df_alim, x="Estabelecimento", y="Valor", text_auto='.2f', color="Estabelecimento")
        st.plotly_chart(fig_alim, use_container_width=True)
