import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título principal de la app
st.set_page_config(page_title="COVID-19 en España", layout="wide")
st.title("📊 Dashboard de COVID-19 en España")

# Cargar datos
@st.cache_data
def load_data():
    historico = pd.read_csv("data/casos_hosp_uci_def_sexo_edad_provres.csv")
    reciente = pd.read_csv("data/hosp_uci_def_sexo_edad_provres_todas_edades.csv")
    df = pd.concat([historico, reciente], ignore_index=True)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.groupby(["provincia_iso", "fecha"])[["num_hosp", "num_uci", "num_def"]].sum().reset_index()
    mapa_provincias = {
        "AN": "Andalucía", "AR": "Aragón", "AS": "Asturias", "IB": "Baleares", "CN": "Canarias", "CB": "Cantabria",
        "CM": "Castilla-La Mancha", "CL": "Castilla y León", "CT": "Cataluña", "VC": "Comunidad Valenciana",
        "EX": "Extremadura", "GA": "Galicia", "MD": "Madrid", "MC": "Murcia", "NC": "Navarra", "PV": "País Vasco",
        "RI": "La Rioja", "CE": "Ceuta", "ML": "Melilla"
    }
    df["comunidad"] = df["provincia_iso"].map(mapa_provincias)
    df = df.dropna(subset=["comunidad"])
    return df

df = load_data()

# Sidebar de opciones
comunidades = df["comunidad"].unique()
comunidad = st.selectbox("Selecciona la comunidad autónoma", sorted(comunidades))

metrica = st.selectbox("Selecciona la métrica", ["Hospitalizados", "UCI", "Fallecidos"])
columna = {"Hospitalizados": "num_hosp", "UCI": "num_uci", "Fallecidos": "num_def"}[metrica]

# Slider de fechas
fechas = df["fecha"].sort_values().unique()
fecha_min, fecha_max = fechas[0], fechas[-1]
fecha_rango = st.slider("Rango de fechas", min_value=fecha_min, max_value=fecha_max, value=(fecha_min, fecha_max))

# Filtrar y graficar
df_filtrado = df[(df["comunidad"] == comunidad) &
                 (df["fecha"] >= fecha_rango[0]) &
                 (df["fecha"] <= fecha_rango[1])].copy()
df_filtrado = df_filtrado.sort_values("fecha")
df_filtrado["media_7d"] = df_filtrado[columna].rolling(7).mean()

st.markdown(f"### Evolución de {metrica} en {comunidad}")
fig, ax = plt.subplots()
ax.plot(df_filtrado["fecha"], df_filtrado["media_7d"], color="skyblue", linewidth=2)
ax.set_xlabel("Fecha")
ax.set_ylabel(metrica)
ax.grid(True)
st.pyplot(fig)

# Métricas clave
ultima_fecha = df_filtrado["fecha"].max()
ultimo_valor = df_filtrado[df_filtrado["fecha"] == ultima_fecha][columna].sum()
pico = df_filtrado[columna].max()
promedio = round(df_filtrado[columna].mean(), 2)

st.markdown("### Métricas clave")
st.metric("Casos actuales", f"{int(ultimo_valor)}")
st.metric("Promedio diario", f"{promedio}")
st.metric("Pico máximo", f"{int(pico)}")

# Footer
st.info("Datos obtenidos del Instituto de Salud Carlos III. © 2025")
st.title("📊 Dashboard de COVID-19 en España")
st.markdown("""
Este panel muestra la evolución de la pandemia de COVID-19 en España, por comunidad autónoma y tipo de métrica (hospitalizaciones, UCI, fallecimientos).  
Los datos proceden del Instituto de Salud Carlos III.  
""")
st.markdown("---")
st.markdown("Creado por [Cesar Vida] | (https://github.com/cesarvida/covid-es-comunidades)")
