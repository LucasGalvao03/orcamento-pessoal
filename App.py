import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# Configuração da página
st.set_page_config(page_title="Orçamento & Finanças - Lucas Galvão", page_icon="💎", layout="wide")

st.title("💎 Gestão Financeira Inteligente - Lucas Galvão")

# --- CONEXÃO AUTENTICADA COM GOOGLE SHEETS ---
@st.cache_resource(ttl=60)
def ligar_google_sheets():
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        if "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
            client = gspread.authorize(credentials)
            
            url = st.secrets.get("spreadsheet_url", "https://docs.google.com/spreadsheets/d/1OWDv54r3rt5Csm_Nou1oJbaKfFyZQ_eqvymlC7YMsmw/edit?usp=sharing")
            sheet = client.open_by_url(url)
            return sheet
        else:
            st.error("⚠️ Configuração 'gcp_service_account' não encontrada nas Secrets do Streamlit.")
            return None
    except Exception as e:
        st.error(f"⚠️ Erro ao autenticar com o Google Sheets: {e}")
        return None

doc_sheets = ligar_google_sheets()

# --- FUNÇÕES DE LEITURA E GRAVAÇÃO ---
def carregar_dados_aba(nome_aba):
    if doc_sheets:
        try:
            worksheet = doc_sheets.worksheet(nome_aba)
            dados = worksheet.get_all_records()
            if dados:
                return pd.DataFrame(dados)
        except Exception:
            pass
    return pd.DataFrame()

def guardar_dados_aba(nome_aba, df):
    if doc_sheets:
        try:
            try:
                worksheet = doc_sheets.worksheet(nome_aba)
            except gspread.WorksheetNotFound:
                worksheet = doc_sheets.add_worksheet(title=nome_aba, rows="100", cols="20")
            
            worksheet.clear()
            # Substitui valores NaN por vazios para evitar erros de serialização JSON
            df_limpo = df.fillna("")
            worksheet.update([df_limpo.columns.values.tolist()] + df_limpo.values.tolist())
            return True
        except Exception as e:
            st.error(f"Erro ao gravar na folha de cálculo: {e}")
    return False

# --- NAVEGAÇÃO LATERAL ---
st.sidebar.header("📅 Navegação do Orçamento")

# Lista de abas da planilha
lista_meses = ["JUNHO - 2026", "JULHO - 2026", "AGOSTO - 2026", "SETEMBRO - 2026"]
mes_selecionado = st.sidebar.selectbox("Escolha o Mês / Aba:", lista_meses)

# Inicialização do Session State isolado por mês
if "dados_meses" not in st.session_state:
    st.session_state.dados_meses = {}

# Carrega os dados do Google Sheets caso ainda não estejam em memória
if mes_selecionado not in st.session_state.dados_meses:
    df_carregado = carregar_dados_aba(mes_selecionado)
    if not df_carregado.empty:
        st.session_state.dados_meses[mes_selecionado] = df_carregado
    else:
        # Estrutura base de salvaguarda
        st.session_state.dados_meses[mes_selecionado] = pd.DataFrame([
            {"Conta": "ITAU (CARD)", "Fatura": 149.67, "Valor Pago": 149.67, "Status": "PAGO", "Data": "30/06/2026", "Extrato": "Tênis Nike"},
            {"Conta": "NUBANK (CARD)", "Fatura": 873.03, "Valor Pago": 873.03, "Status": "PAGO", "Data": "30/06/2026", "Extrato": "Mercado Livre"},
            {"Conta": "HONDA CONSORCIO", "Fatura": 659.68, "Valor Pago": 659.68, "Status": "PAGO", "Data": "15/06/2026", "Extrato": "Consórcio Moto"}
        ])

df_atual = st.session_state.dados_meses[mes_selecionado]

# Botão de Sincronização Manual na Barra Lateral
st.sidebar.divider()
if st.sidebar.button("☁️ Recarregar do Google Sheets"):
    st.cache_resource.clear()
    st.session_state.dados_meses.pop(mes_selecionado, None)
    st.rerun()

st.caption(f"A exibir dados da aba: **{mes_selecionado}**")

# TABS DE VISUALIZAÇÃO E EDIÇÃO
tab_dash, tab_contas = st.tabs(["📈 Dashboard & Saldo", "💳 Gestão de Contas & Tabela"])

total_faturas = df_atual['Fatura'].sum() if 'Fatura' in df_atual.columns else 0.0
total_pago = df_atual['Valor Pago'].sum() if 'Valor Pago' in df_atual.columns else 0.0

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.subheader(f"⚡ Resumo Executivo - {mes_selecionado}")
    c1, c2 = st.columns(2)
    c1.metric("Total Faturado", f"R$ {total_faturas:,.2f}")
    c2.metric("Total Efectivamente Pago", f"R$ {total_pago:,.2f}")
    st.divider()

    if not df_atual.empty and 'Status' in df_atual.columns:
        fig_status = px.pie(df_atual, names='Status', values='Fatura', hole=0.4, title="Distribuição de Faturas por Status")
        st.plotly_chart(fig_status, width="stretch")

# --- TAB 2: EDITAR TABELA E GRAVAR ---
with tab_contas:
    st.subheader(f"💳 Tabela Editável - {mes_selecionado}")
    st.info("💡 Faça as edições necessárias na tabela abaixo. Quando terminar, clique no botão **'💾 Gravar Alterações na Folha de Cálculo'** para salvar permanentemente na nuvem.")

    df_editado = st.data_editor(
        df_atual,
        num_rows="dynamic",
        column_config={
            "Conta": st.column_config.TextColumn("Conta / Banco"),
            "Fatura": st.column_config.NumberColumn("Fatura (R$)", format="R$ %.2f"),
            "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f"),
            "Status": st.column_config.SelectboxColumn("Status", options=["PAGO", "PENDENTE", "ISENTO"]),
            "Data": st.column_config.TextColumn("Vencimento / Data"),
            "Extrato": st.column_config.TextColumn("Extrato / Observações")
        },
        width="stretch",
        key=f"editor_final_{mes_selecionado}"
    )

    # Atualiza a memória local
    st.session_state.dados_meses[mes_selecionado] = df_editado

    st.divider()
    
    # Botão explícito de gravação para garantir que a API do Google processa o lote completo
    if st.button("💾 Gravar Alterações na Folha de Cálculo", type="primary", use_container_width=True):
        with st.spinner("A gravar dados no Google Sheets..."):
            sucesso = guardar_dados_aba(mes_selecionado, df_editado)
            if sucesso:
                st.success(f"✅ Alterações da aba **'{mes_selecionado}'** salvas com sucesso na Google Sheets!")
            else:
                st.error("❌ Falha ao gravar na folha de cálculo. Verifique as credenciais nas Secrets.")
