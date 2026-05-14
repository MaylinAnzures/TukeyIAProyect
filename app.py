import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config( #modificamos nuestra pag
    page_title="Dashboard", 
    page_icon=":bar_chart:" #el favicon de la pag
)
st.title("Dashboard How AI is Changing Student Life:bar_chart:")

#nuestra descripcion del dataset
st.header(":pushpin: Acerca de este dataset")
st.write("""Este conjunto de datos explora cómo la inteligencia artificial está transformando la vida estudiantil, centrándose en los hábitos de estudio, el rendimiento académico y la satisfacción general. Ofrece información sobre cómo los estudiantes interactúan con las herramientas de IA en sus rutinas diarias de aprendizaje y cómo estas herramientas influyen en sus resultados. El conjunto de datos destaca patrones de uso reales y revela tanto los beneficios como los posibles inconvenientes de la adopción de la IA en la educación.""")

df = pd.read_csv("/home/maylinanzures/ejercicio5/TukeyIAProyect/AI_Student_Life_Pakistan_2026.csv")

st.subheader("1. Análisis de Impacto por Herramienta")


# a mi lista le agrego Todas las ciudades
paises = list(df['City'].unique())
lista_paises = ["Todas las ciudades"] + paises
ciudad_sel = st.selectbox("Selecciona una Ciudad:", options=lista_paises)

if ciudad_sel == "Todas las ciudades":
    df_filtrado = df
else:
    df_filtrado = df[df['City'] == ciudad_sel]


#preparamos los datos para el bar_chart
df_IA = df_filtrado.groupby('AI_Tool_Used')['Impact_on_Grades'].value_counts(normalize=True).unstack()

#Streamlit usa sus propios colores  :o
st.bar_chart(df_IA, x_label="Herramienta IA", y_label="Impacto en las notas")

st.subheader("2. Comparativa de Propósitos: Coding vs. Writing")

lista_propositos = list(df['Purpose'].unique()) #lista de los propositos

prop_sel = st.radio(
    "Selecciona el propósito de uso de la IA:",
    options=lista_propositos,
    horizontal=True 
)

df_filtrado_p = df[df['Purpose'] == prop_sel]
conteo_impacto = df_filtrado_p['Impact_on_Grades'].value_counts()

#ojo para st.bar_chart en un solo grupo, lo ideal es pasar una serie
st.bar_chart(conteo_impacto, x_label="Cambio en las notas", y_label="Cantidad de alumnos")

st.subheader("3. Análisis de Anomalías: Alta Satisfacción y Notas en Declive ")

#filtramos y escogemos columnas que necesitaamos
dfAS_ND = df[(df['Satisfaction_Level'] == 'High') & (df['Impact_on_Grades'] == 'Slight Decline')][['Satisfaction_Level', 'Impact_on_Grades', 'AI_Tool_Used', 'Daily_Usage_Hours']]

#usamos el min y max del df ya filtrado
min_uso = float(dfAS_ND['Daily_Usage_Hours'].min())
max_uso = float(dfAS_ND['Daily_Usage_Hours'].max())


horas_seleccionadas = st.slider(
    "Filtrar por horas de uso diario:",
    min_value=min_uso,
    max_value=max_uso,
    value=min_uso,
    step=0.5 #ananzamos de 0.5
)

#el df con la hora seleccionada
df_final = dfAS_ND[dfAS_ND['Daily_Usage_Hours'] >= horas_seleccionadas]

st.write(f"Estudiantes encontrados con {horas_seleccionadas} horas o más: {len(df_final)}")

#excluimos las col
st.dataframe(df_final[['AI_Tool_Used', 'Daily_Usage_Hours']])

st.subheader("4. Demografía y Uso")

dimensiones = []

#los checkboxes llenan esa lista
if st.checkbox("Desglosar por sexo", value=True):
    dimensiones.append('Gender')

if st.checkbox("Desglosar por Nivel Educativo"):
    dimensiones.append('Education_Level')

# para agrupar
if dimensiones:
    #agrupamos por las col en nuestra litsa y el promedio de horas, el reset para agregar indices 0 1
    df_resumen = df.groupby(dimensiones)['Daily_Usage_Hours'].mean().reset_index()
    if len(dimensiones) > 1:
        #si hay dos, el segundo se convierte en el color de las barras
        st.bar_chart(
            df_resumen, 
            x=dimensiones[0], 
            y='Daily_Usage_Hours',
            y_label="Promedio de Horas",
            color=dimensiones[1],
            stack=False #esto las pone una al lado de la otra para comparar mejor
        )
    else:
        #grafica normal si solo es 1 checked
        st.bar_chart(df_resumen, x=dimensiones[0], y='Daily_Usage_Hours', y_label="Promedio de Horas")
else:
    #si no se marc nada mostramos solo el promedio general en un metric
    promedio_gral = df['Daily_Usage_Hours'].mean()
    st.metric("Promedio General de Uso (Horas)", f"{promedio_gral:.2f}")

st.subheader("5. Rendimiento Regional")
#reutilizamos nuetsra lista paises
ciudades_seleccionadas = st.multiselect(
    "Selecciona ciudades para comparar:",
    options=paises,
    default=paises[:2] #dos marcadas por defecto
)

if ciudades_seleccionadas:
    df_regional = df[df['City'].isin(ciudades_seleccionadas)]
    
    #sacamos el total de estudiantes por ciudad
    total_por_ciudad = df_regional.groupby('City')['Impact_on_Grades'].count()

    #positivos por ciudad
    positivos_por_ciudad = df_regional[df_regional['Impact_on_Grades'] == 'Improved'].groupby('City')['Impact_on_Grades'].count()

    #calculamos el porcentaje: (Positivos / Total) * 100 esto segun san google
    # .fillna(0) es por si una ciudad no tiene niun positivo, para que no salga error
    rendimiento = (positivos_por_ciudad / total_por_ciudad * 100).fillna(0).reset_index(name='Porcentaje_Mejora')

    rendimiento = rendimiento.sort_values(by='Porcentaje_Mejora', ascending=False)
    st.bar_chart(rendimiento, x='City', y='Porcentaje_Mejora', x_label="Ciudad", y_label="Porcentaje de Merjoa")
else:
    st.warning("Selecciona al menos una ciudad para ver la comparativa.")

#insights
st.divider()
st.header("Descubrimientos Clave")

with st.expander("Ver Insights del Análisis"):
    st.markdown("""
    1. **El Paradox de la Satisfacción:** Existe un grupo crítico de estudiantes que reportan una satisfacción 'Alta' con la IA, pero sus notas muestran un 'Ligero Declive'. Esto sugiere que la IA podría estar generando una falsa sensación de competencia o exceso de confianza.
    2. **Efecto de la Saturación Horaria:** El análisis de demografía revela que, después de las 5-6 horas de uso diario, el impacto positivo en las notas tiende a estancarse o disminuir, lo que indica un 'punto de retorno decreciente'.
    3. **Especialización por Propósito:** Herramientas orientadas a *Coding* muestran una mayor tasa de impacto positivo en comparación con las de *Writing*, posiblemente porque la IA en programación actúa como un tutor de lógica, mientras que en escritura puede derivar en un reemplazo del esfuerzo crítico.
    """)