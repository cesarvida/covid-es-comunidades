import streamlit as st
import pandas as pd

st.set_page_config(page_title="COVID España", layout="centered")
st.title("📊 Dashboard de COVID-19 en España")
st.success("La app se ha cargado correctamente.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/casos_hosp_uci_def_sexo_edad_provres.csv")
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df

df = load_data()

st.subheader("Vista previa de los datos (5 primeras filas)")
st.dataframe(df.head())
