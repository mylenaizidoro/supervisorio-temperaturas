import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Supervisório Industrial", page_icon="🌡️", layout="wide")

if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

API_GET_URL = "https://eight-planes-cut.loca.lt/temperaturas"
HEADERS = {"serveo-skip-browser-warning": "true"}

# ---------------------------------------------------------
# TELA 1: MENU PRINCIPAL (SELEÇÃO DE MÁQUINAS)
# ---------------------------------------------------------
if st.session_state.pagina == "home":
    st.title("🏭 Central de Supervisão - Células Industriais")
    st.write("Selecione abaixo a máquina que deseja monitorar em tempo real:")
    
    st.markdown("---")
    
    if st.button("🔥 Máquina de Solda - Temperaturas", use_container_width=True):
        st.session_state.pagina = "solda"
        st.rerun()
        
    if st.button("📊 PH02 - Dash", use_container_width=True):
        st.session_state.pagina = "outra"
        st.rerun()
        
    if st.button("🛡️ PH09 - Isolant Plancher", use_container_width=True):
        st.session_state.pagina = "outra"
        st.rerun()
        
    if st.button("⚙️ PH20 - XDF", use_container_width=True):
        st.session_state.pagina = "outra"
        st.rerun()
        
    if st.button("🔧 PH03 - Isolador Tcross", use_container_width=True):
        st.session_state.pagina = "outra"
        st.rerun()

# ---------------------------------------------------------
# TELA 2: APENAS O PAINEL DE TEMPERATURAS DA MÁQUINA DE SOLDA
# ---------------------------------------------------------
elif st.session_state.pagina == "solda":
    if st.button("⬅️ Voltar para a Seleção de Máquinas"):
        st.session_state.pagina = "home"
        st.rerun()

    st.title("🔥 Supervisório - Máquina de Solda (Temperaturas)")
    st.write("Acompanhamento em tempo real dos canais do CLP Delta DVP-12SE.")

    status_placeholder = st.empty()
    cards_placeholder = st.empty()
    grafico_placeholder = st.empty()

    try:
        response = requests.get(API_GET_URL, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            historico_bruto = response.json()
            
            if historico_bruto and isinstance(historico_bruto, list):
                dados_formatados = []
                for item in historico_bruto:
                    linha = {"timestamp": item.get("timestamp", "")}
                    for i in range(1, 18):
                        linha[f"Sensor {i}"] = item.get(f"sensor_{i}", 0.0)
                    dados_formatados.append(linha)
                
                df = pd.DataFrame(dados_formatados)
                
                status_placeholder.success(f"Última sincronização com a API: {df['timestamp'].iloc[-1]}")
                
                with cards_placeholder.container():
                    st.subheader("📊 Valores Atuais por Sensor")
                    ultima_linha = df.iloc[-1]
                    cols = st.columns(6)
                    for idx, col in enumerate(cols):
                        if idx < 17:
                            sensor_nome = f"Sensor {idx+1}"
                            val = ultima_linha[sensor_nome]
                            col.metric(label=sensor_nome, value=f"{val} °C")

                with grafico_placeholder.container():
                    st.subheader("📈 Análise Gráfica dos Sensores")
                    
                    aba_linhas, aba_barras = st.tabs(["📈 Gráfico de Linhas (Tendência)", "📊 Gráfico de Barras (Comparativo)"])
                    
                    df_plot = df.set_index("timestamp")
                    
                    with aba_linhas:
                        st.line_chart(df_plot)
                        
                    with aba_barras:
                        df_barras = ultima_linha.drop("timestamp")
                        st.bar_chart(df_barras)
            else:
                status_placeholder.warning("⚠️ A API conectou, mas o histórico de dados ainda está vazio.")
        else:
            status_placeholder.warning(f"⚠️ A API respondeu com o código de status: {response.status_code}")

    except Exception as e:
        status_placeholder.error(f"❌ Erro ao conectar com a API FastAPI: {e}")

# ---------------------------------------------------------
# TELA 3: AVISO PARA AS OUTRAS MÁQUINAS
# ---------------------------------------------------------
else:
    if st.button("⬅️ Voltar para a Seleção de Máquinas"):
        st.session_state.pagina = "home"
        st.rerun()

    st.title("⚙️ Célula em Desenvolvimento")
    st.info("ℹ️ Esta máquina ainda não possui o supervisório de temperaturas integrado. Volte em breve!")
