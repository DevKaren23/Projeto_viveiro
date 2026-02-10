import streamlit as st
import requests

st.set_page_config(
    page_title="Viveiro de Mudas",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

API_URL = ""

st.title("🌳 Viveiro de Mudas Florestais")

menu = st.radio(
    "O que você quer fazer?",
    ["🌱 Espécie", "📦 Lote", "🧪 Qualidade"],
    horizontal=False
)

if menu == "🌱 Espécie":
    st.header("🌱 Nova Espécie")

    with st.form("form_especie"):
        nome_popular = st.text_input("Nome popular")
        nome_cientifico = st.text_input("Nome científico")

        submitted = st.form_submit_button("💾 Salvar Espécie")

    if submitted:
        requests.post(
            f"{API_URL}/especies/",
            params={
                "nome_popular": nome_popular,
                "nome_cientifico": nome_cientifico
            }
        )
        st.success("Espécie salva com sucesso!")

    try:
        especies = requests.get(f"{API_URL}/especies/").json()
        if especies:
            for e in especies:
                st.write(f"🌱 {e['nome_popular']} — *{e['nome_cientifico']}*")
        else:
            st.info("Nenhuma espécie cadastrada ainda.")
    except:
        st.error("Não foi possível carregar as espécies.")


elif menu == "📦 Lote":
    st.header("📦 Novo Lote")

    especies = requests.get(f"{API_URL}/especies/").json()

    with st.form("form_lote"):
        especie = st.selectbox(
            "Espécie",
            especies,
            format_func=lambda x: x["nome_popular"]
        )

        quantidade = st.number_input("Quantidade", min_value=1)
        estagio = st.selectbox(
            "Estágio",
            ["Germinação", "Crescimento", "Rustificação", "Pronta"]
        )
        local = st.text_input("Local / Canteiro")

        submitted = st.form_submit_button("💾 Salvar Lote")

    if submitted:
        requests.post(
            f"{API_URL}/lotes/",
            params={
                "especie_id": especie["id"],
                "quantidade": quantidade,
                "estagio": estagio,
                "local": local
            }
        )
        st.success("Lote cadastrado!")

elif menu == "🧪 Qualidade":
    st.header("🧪 Avaliação de Qualidade")

    with st.form("form_qualidade"):
        lote_id = st.number_input("ID do Lote", min_value=1)
        altura = st.number_input("Altura média (cm)")
        diametro = st.number_input("Diâmetro do coleto (mm)")

        sanidade = st.radio(
            "Sanidade",
            ["Boa", "Pragas", "Doenças"]
        )

        uniformidade = st.radio(
            "Uniformidade",
            ["Boa", "Média", "Ruim"]
        )

        nota = st.slider("Nota de qualidade", 0.0, 10.0)
        obs = st.text_area("Observações")

        submitted = st.form_submit_button("✅ Registrar Avaliação")

    if submitted:
        requests.post(
            f"{API_URL}/qualidade/",
            params={
                "lote_id": lote_id,
                "altura_media": altura,
                "diametro_coleto": diametro,
                "sanidade": sanidade,
                "uniformidade": uniformidade,
                "nota_qualidade": nota,
                "observacoes": obs
            }
        )
        st.success("Avaliação registrada!")

