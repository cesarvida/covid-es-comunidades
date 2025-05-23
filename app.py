import streamlit as st
import pandas as pd

st.set_page_config(page_title="COVID España", layout="centered")
st.title("📊 Dashboard de COVID-19 en España")
st.success("La app se ha cargado correctamente.")

@st.cache_data
def load_data():
    df1 = pd.read_csv("data/casos_hosp_uci_def_sexo_edad_provres.csv")
    df2 = pd.read_csv("data/hosp_uci_def_sexo_edad_provres_todas_edades.csv")
    df = pd.concat([df1, df2], ignore_index=True)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df

df = load_data()

# Mapeo de provincias a comunidades (simple)
mapa = {
    "M": "Madrid", "B": "Cataluña", "V": "Comunidad Valenciana", "SE": "Andalucía",
    "Z": "Aragón", "LO": "La Rioja", "BI": "País Vasco", "O": "Asturias",
    "C": "Galicia", "SA": "Castilla y León", "TO": "Castilla-La Mancha"
}
df["comunidad"] = df["provincia_iso"].map(mapa)

# Eliminar filas sin comunidad identificada
df = df.dropna(subset=["comunidad"])

# Filtros
comunidades = sorted(df["comunidad"].unique())
comunidad = st.selectbox("Selecciona la comunidad autónoma", comunidades)

metricas = {
    "Hospitalizados": "num_hosp",
    "Ingresos UCI": "num_uci",
    "Defunciones": "num_def"
}
metrica_legible = st.selectbox("Selecciona la métrica", list(metricas.keys()))
metrica = metricas[metrica_legible]

# Filtro de fechas
fechas = pd.to_datetime(df["fecha"].dropna().sort_values().unique())
fecha_min = fechas.min()
fecha_max = fechas.max()

fecha_rango = st.slider(
    "Rango de fechas",
    min_value=fecha_min,
    max_value=fecha_max,
    value=(fecha_min, fecha_max)
)



# Filtrar y agrupar
df_filtrado = df[
    (df["comunidad"] == comunidad) &
    (df["fecha"] >= fecha_rango[0]) &
    (df["fecha"] <= fecha_rango[1])
]
df_agregado = df_filtrado.groupby("fecha")[metrica].sum().reset_index()
df_agregado["media_7d"] = df_agregado[metrica].rolling(window=7).mean()

# Gráfico
st.subheader(f"Evolución de {metrica_legible} en {comunidad}")
st.line_chart(df_agregado.set_index("fecha")["media_7d"])

