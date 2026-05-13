import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#1 Analisis de Impacto por Herramienta (Filtros de Área Geográfica)
st.set_page_config( #modificamos nuestra pag
    page_title="Dashboard", 
    page_icon=":bar_chart:" #el favicon de la pag
)
st.title("Dashboard How AI is Changing Student Life:bar_chart:")

#nuestra descripcion del dataset
st.header(":pushpin: Acerca de este dataset")
st.write("""Este conjunto de datos explora cómo la inteligencia artificial está transformando la vida estudiantil, centrándose en los hábitos de estudio, el rendimiento académico y la satisfacción general. Ofrece información sobre cómo los estudiantes interactúan con las herramientas de IA en sus rutinas diarias de aprendizaje y cómo estas herramientas influyen en sus resultados. El conjunto de datos destaca patrones de uso reales y revela tanto los beneficios como los posibles inconvenientes de la adopción de la IA en la educación.""")

df = pd.read_csv("/home/maylinanzures/ejercicio5/TukeyIAProyect/AI_Student_Life_Pakistan_2026.csv")

st.subheader("1. Análisis de Impacto por Herramienta (Filtros de Área Geográfica)")


# a mi lista le agrego Todas las ciudades
lista_paises = ["Todas las ciudades"] + list(df['City'].unique())
ciudad_sel = st.selectbox("Selecciona una Ciudad:", options=lista_paises)

if ciudad_sel == "Todas las ciudades":
    df_filtrado = df
else:
    df_filtrado = df[df['City'] == ciudad_sel]

df_IA = df_filtrado.groupby('AI_Tool_Used')['Impact_on_Grades'].value_counts(normalize=True).unstack()

fig, ax = plt.subplots(figsize=(7,4))

df_IA.plot(kind='bar', stacked=True, ax=ax, color=['#20c1d8','#943164','#ffcef3'])

ax.set_title(f"Distribución de Impacto en {ciudad_sel}")
ax.set_xlabel("Herramienta de IA")
ax.legend(title="Impacto", bbox_to_anchor=(1, 1), loc='upper left') #leyenda afuera

plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("2. Comparativa de Propósitos: Coding vs. Writing")

#obtener los propositos en lista, al parecer es mas facil asi
lista_propositos = list(df['Purpose'].unique())

#creamos los radiobutton
prop_sel = st.radio(
    "Selecciona el propósito de uso de la IA:",
    options=lista_propositos,
    horizontal=True # pa que salgan en linea
)

#Filtaromos segun la eleccion
df_filtrado_p = df[df['Purpose'] == prop_sel]

#calculamos por eleccion seleccionada
#no necesitamos unstack porque es un solo grupo :o
conteo_impacto = df_filtrado_p['Impact_on_Grades'].value_counts()

fig, ax = plt.subplots(figsize=(7, 4))


conteo_impacto.plot(kind='bar', ax=ax, color=['#ff765e','#d44e29','#ffff7b'])

ax.set_title(f"Impacto en Notas para: {prop_sel}")
ax.set_ylabel("Cantidad de Estudiantes")
ax.set_xlabel("Tipo de Impacto")
ax.legend(title="Impacto", bbox_to_anchor=(1, 1), loc='upper left') 

plt.xticks(rotation = 0)
st.pyplot(fig)

st.subheader("3. Análisis de Anomalías: Alta Satisfacción y Notas en Declive ")
# 1. Filtro base de la anomalía (Guardamos todas las columnas necesarias)
df_anomalia_base = df[(df['Satisfaction_Level'] == 'High') & (df['Impact_on_Grades'] == 'Slight Decline')]

# 2. Configurar el slider interactivo
# Usamos los valores reales de tus datos para los límites del slider
min_h = float(df['Daily_Usage_Hours'].min())
max_h = float(df['Daily_Usage_Hours'].max())

horas_corte = st.slider(
    "Selecciona el mínimo de horas de uso diario para analizar:", 
    min_value=min_h, 
    max_value=max_h, 
    value=min_h, # Inicia en el mínimo para mostrar a todos al principio
    step=0.5
)

# 3. Aplicar el filtro del slider al DataFrame de la anomalía
dfAS_ND = df_anomalia_base[df_anomalia_base['Daily_Usage_Hours'] >= horas_corte]

# --- VISUALIZACIÓN EN STREAMLIT ---

st.subheader("3. Análisis de Anomalías: Alta Satisfacción, Notas en Declive")

# Muestra cuántos son (Componente visual de conteo)
col_metric, _ = st.columns([1, 2])
with col_metric:
    st.metric("Est```

---

### Explicación de qué hicimos con la lógica:

1.  **El Slider como "Filtro Acumulativo"udiantes encontrados", len(dfAS_ND))

# Tabla detallada (Componente visual de datos)
# Seleccionamos las columnas que pide el ejercicio para**: Al usar `>= horas_filtro`, permites que el usuario vea a todos los que superan ese tiempo de uso. Esto es clave para el análisis porque que la tabla sea clara
st.write(f"Mostrando estudiantes con {horas_corte} horas o más de uso:")
st.dataframe(dfAS_ND[['AI_Tool_Used', 'Daily_Usage_Hours', 'Satisfaction_Level', 'Impact_on_Grades']])