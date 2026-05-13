import streamlit as st
import pandas as pd
import numpy as np



#1 Analisis de Impacto por Herramienta (Filtros de Área Geográfica)
st.set_page_config( #modificamos nuestra pag
    page_title="Dashboard", 
    page_icon=":bar_chart:", #el favicon de la pag
    layout="wide",  # el layout es mas acho
)
st.title("Dashboard How AI is Changing Student Life:bar_chart:")

#nuestra descripcion del dataset
st.header(":pushpin: Acerca de este dataset")
st.write("""Este conjunto de datos explora cómo la inteligencia artificial está transformando la vida estudiantil, centrándose en los hábitos de estudio, el rendimiento académico y la satisfacción general. Ofrece información sobre cómo los estudiantes interactúan con las herramientas de IA en sus rutinas diarias de aprendizaje y cómo estas herramientas influyen en sus resultados. El conjunto de datos destaca patrones de uso reales y revela tanto los beneficios como los posibles inconvenientes de la adopción de la IA en la educación.""")

df = pd.read_csv("/home/maylinanzures/ejercicio5/TukeyIAProyect/AI_Student_Life_Pakistan_2026.csv")

"""
# 1. Filtro base (Satisfacción Alta y Notas en Declive)
# Incluimos Daily_Usage_Hours para poder usarla en el slider
dfAS_ND = df[(df['Satisfaction_Level'] == 'High') & (df['Impact_on_Grades'] == 'Slight Decline')][['Satisfaction_Level', 'Impact_on_Grades', 'AI_Tool_Used','Daily_Usage_Hours']]

# 2. Definimos el slider (basado en el rango real de tus datos)
min_h = float(dfAS_ND['Daily_Usage_Hours'].min())
max_h = float(dfAS_ND['Daily_Usage_Hours'].max())

horas_corte = st.slider('Selecciona el mínimo de horas de uso diario:', min_h, max_h, min_h)

# 3. Aplicamos el segundo filtro sobre el DataFrame ya filtrado
df_filtrado_final = dfAS_ND[dfAS_ND['Daily_Usage_Hours'] >= horas_corte]

# 4. Mostramos los resultados (Cantidad y Tabla)
st.subheader("Resultados del Análisis")
st.write(f"Se encontraron **{len(df_filtrado_final)}** estudiantes con {horas_corte} horas o más.")

st.dataframe(df_filtrado_final[['AI_Tool_Used', 'Daily_Usage_Hours', 'Satisfaction_Level']]) """