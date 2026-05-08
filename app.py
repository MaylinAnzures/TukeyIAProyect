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
df
