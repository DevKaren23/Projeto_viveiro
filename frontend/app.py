import streamlit as st


st.set_page_config(
    page_title="Viveiro de Mudas",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

API_URL = ""

st.title("🌳 Viveiro de Mudas Florestais")

import sqlite3

conn = sqlite3.connect("viveiro.db", check_same_thread=False)
cursor = conn.cursor()

# -------------------------------
# TABELA DE ESPÉCIES
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_popular TEXT NOT NULL,
    nome_cientifico TEXT NOT NULL,
    observacoes TEXT,
    data_cadastro TEXT
)
""")

# -------------------------------
# TABELA DE LOTES
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS lotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_id INTEGER NOT NULL,
    codigo_lote TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    data_semeadura TEXT,
    status TEXT,
    FOREIGN KEY (especie_id) REFERENCES especies (id)
)
""")

# -------------------------------
# TABELA DE QUALIDADE
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS qualidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lote_id INTEGER NOT NULL,
    altura REAL,
    diametro REAL,
    sanidade TEXT,
    vigor TEXT,
    nota REAL,
    classificacao TEXT,
    data_avaliacao TEXT,
    FOREIGN KEY (lote_id) REFERENCES lotes (id)
)
""")

conn.commit()


menu = st.radio(
    "O que você quer fazer?",
    {
        "🌱 Espécie": "especie",
        "📦 Lote": "lote",
        "🧪 Qualidade": "qualidade"
    }.keys()
)

menu_valor = {
    "🌱 Espécie": "especie",
    "📦 Lote": "lote",
    "🧪 Qualidade": "qualidade"
}[menu]


if menu_valor == "especie":
    st.header("🌱 Nova Espécie")

    nome_popular = st.text_input("Nome popular")
    nome_cientifico = st.text_input("Nome científico")

    if st.button("Salvar espécie"):
        if nome_popular and nome_cientifico:
            cursor.execute(
                "INSERT INTO especies (nome_popular, nome_cientifico) VALUES (?, ?)",
                (nome_popular, nome_cientifico)
            )
            conn.commit()
            st.success("Espécie cadastrada com sucesso!")
        else:
            st.warning("Preencha todos os campos")


elif menu == "📦 Lote":
    st.header("📦 Novo Lote")

    cursor.execute("SELECT id, nome_popular FROM especies")
    especies = cursor.fetchall()

    if not especies:
        st.warning("Cadastre uma espécie primeiro.")
    else:
        especie_escolhida = st.selectbox(
            "Espécie",
            especies,
            format_func=lambda x: x[1]
        )

        codigo_lote = st.text_input("Código do lote")
        quantidade = st.number_input("Quantidade de mudas", min_value=1, step=1)
        data_semeadura = st.date_input("Data da semeadura")
        status = st.selectbox(
            "Status do lote",
            ["Em produção", "Pronto", "Descartado"]
        )

        if st.button("Salvar lote"):
            if codigo_lote:
                cursor.execute("""
                    INSERT INTO lotes
                    (especie_id, codigo_lote, quantidade, data_semeadura, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    especie_escolhida[0],
                    codigo_lote,
                    quantidade,
                    data_semeadura.isoformat(),
                    status
                ))

                conn.commit()
                st.success("Lote cadastrado com sucesso!")
            else:
                st.warning("Informe o código do lote.")


elif menu_valor == "qualidade":
    st.header("🧪 Avaliação de Qualidade")

    # Buscar espécies
    cursor.execute("SELECT id, nome_popular FROM especies")
    especies = cursor.fetchall()

    if not especies:
        st.warning("Cadastre uma espécie antes de avaliar.")
    else:
        especie = st.selectbox(
            "Espécie",
            especies,
            format_func=lambda x: x[1]
        )

        altura = st.number_input("Altura da muda (cm)", min_value=0.0)
        diametro = st.number_input("Diâmetro do colo (mm)", min_value=0.0)

        sanidade = st.selectbox("Estado fitossanitário", ["Boa", "Regular", "Ruim"])
        vigor = st.selectbox("Vigor", ["Alto", "Médio", "Baixo"])

        if st.button("Calcular e salvar avaliação"):
            nota = 0

            if altura >= 30:
                nota += 3
            if diametro >= 3:
                nota += 3

            nota += {"Boa": 2, "Regular": 1, "Ruim": 0}[sanidade]
            nota += {"Alto": 2, "Médio": 1, "Baixo": 0}[vigor]

            if nota >= 8:
                classificacao = "A"
            elif nota >= 6:
                classificacao = "B"
            elif nota >= 4:
                classificacao = "C"
            else:
                classificacao = "Reprovada"

            cursor.execute("""
                INSERT INTO qualidade 
                (especie_id, altura, diametro, sanidade, vigor, nota, classificacao, data_avaliacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, date('now'))
            """, (
                especie[0],
                altura,
                diametro,
                sanidade,
                vigor,
                nota,
                classificacao
            ))

            conn.commit()

            st.success(f"Nota: {nota} | Classificação: {classificacao}")


