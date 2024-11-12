import streamlit as st
import pandas as pd

# Configuración de la página web
st.set_page_config(
    page_title="EL CATALOGO SISMICO PERÚ 1960-2023 (IGP)",
    page_icon="🌍",
   
)

# Introducción de la aplicación web
st.write("""
    Esta página web proporciona acceso al dataset 'Catálogo Sísmico 1960-2023 (IGP)',
          con información detallada sobre los sismos registrados, incluyendo mapas 
         de epicentros organizados por año, magnitud y profundidad. Además, ofrece 
         gráficos interactivos que analizan la actividad sísmica en función de la 
         magnitud, profundidad y fecha, y permite filtrar los datos según estos criterios, 
         facilitando un análisis preciso y personalizado.
""")

# Título principal de la aplicación
st.title("EL CATALOGO SISMICO EN EL PERÚ (1960-2023) (IGP)")

st.write("""El Perú, al ubicarse en la zona de interacción de 
         las placas de Nazca y Sudamericana, es un país sísmico 
         que ha experimentado sismos de gran magnitud, ocasionando 
         graves daños en infraestructura y pérdidas de vidas humanas. 
         Por esta razón, es fundamental contar con un registro 
         detallado de los sismos ocurridos en los últimos años, 
         que permita estar mejor preparados para futuros eventos. 
         En este contexto, se ha decidido realizar un catálogo sísmico 
         para recopilar y analizar estos sucesos, como herramienta 
         de prevención y apoyo en la toma de decisiones informadas.
         """)

st.write(
    """
    Un catálogo sísmico es una base de datos que contiene todos los 
    parámetros que caracterizan a un sismo, calculados en las mismas 
    condiciones, con el objetivo de constituirse como una base 
    homogénea útil para la realización de estudios en sismología. 
    El presente catálogo ha sido elaborado por el Instituto 
    Geofísico del Perú (IGP), institución responsable del 
    monitoreo de la actividad sísmica en el país, y contiene 
    todos aquellos sismos percibidos por la población y registrados 
    por la Red Sísmica Nacional desde 1960, fecha en la que 
    se inicia la vigilancia instrumental de la sismicidad 
    en el Perú.
    """
)

# Sección para cargar y mostrar el conjunto de datos
st.header("Conjunto de datos")

# Función para cargar los datos del archivo Excel
@st.cache
def load_data():
    url = "CÓDIGO/Dataset_1960_2023.xlsx"
    data_raw = pd.read_excel(url)   # Lee el archivo Excel desde el enlace
    data = data_raw.set_index("ID") # Establece la columna 'ID' como índice
    return data


loading = st.text("Cargando datos ...") # Mensaje mientras los datos se cargan
data = load_data()
st.dataframe(data)
loading.empty()

# El enlace directo al conjunto de datos
st.write("El dataset del catálogo sísmico se encuentra en el siguiente [link](CÓDIGO/Dataset_1960_2023.xlsx)")

# Información sobre las columnas del dataset
st.subheader("Columnas")
st.write(
    """
    - **FECHA_UTC**: Hora universal coordinado (UTC), es la fecha con cinco horas 
        adelantadas con respecto a la hora local debido a que Peru 
        se encuentra en una zona horaria UTC -5. 
    - **HORA_UTC**: Hora universal coordinada (UTC), cinco horas adelantadas 
        con respecto a la hora local debido a que Peru se encuentra 
        en una zona horaria UTC -5.
    - **LATITUD**: Es la distancia en grados, minutos y segundos que hay con 
        respecto al paralelo principal, que es el ecuador (0º). 
        La latitud puede ser norte y sur.
    - **LONGITUD**: Es la distancia en grados, minutos y segundos que hay 
        con respecto al meridiano principal, que es el meridiano de Greenwich (0º).
    - **PROFUNDIDAD**: Profundidad del foco sísmico por debajo de la superficie.
    - **MAGNITUD**: Corresponde a la cantidad de energía liberada por el sismo 
        y esta expresada en la escala de magnitud momento Mw.
    - **FECHA_CORTE**: Fecha de corte de información.
"""
)

# Función para transformar y limpiar los datos
def get_new_data(data):
    FECHA_CORTE = data.at[0, "FECHA_CORTE"]
    data = data.drop(columns=["FECHA_CORTE"], axis=1)
    data["FECHA_UTC"] = pd.to_datetime(data["FECHA_UTC"], format="%Y%m%d")
    data.rename(columns={"LATITUD": "Latitud", "LONGITUD": "Longitud"}, inplace=True)
    # Si la fecha de corte no está en el estado de sesión, la guarda
    if "FECHA_CORTE" not in st.session_state:
        st.session_state["FECHA_CORTE"] = FECHA_CORTE
    
    # Crea nuevas columnas para año, mes, día, hora, minutos y segundos
    new_data = data.copy(deep=True)
    new_data["Año"] = new_data["FECHA_UTC"].dt.year
    new_data["Mes"] = new_data["FECHA_UTC"].dt.month
    new_data["Dia"] = new_data["FECHA_UTC"].dt.day
    new_data["HORA_UTC"] = new_data["HORA_UTC"].astype(str)
    dic_hora = {
        "Hora": [],
        "Minutos": [],
        "Segundos": [],
    }
    for i in new_data["HORA_UTC"]:
        dic_hora["Hora"].append(i[:-4])
        dic_hora["Minutos"].append(i[-4:-2])
        dic_hora["Segundos"].append(i[-2:])
        
    # Elimina las columnas de 'FECHA_UTC' y 'HORA_UTC' y concatena las nuevas columnas de hora
    new_data.drop(["FECHA_UTC"], axis=1, inplace=True)
    new_data.drop(["HORA_UTC"], axis=1, inplace=True)
    new_data = pd.concat([new_data, pd.DataFrame(dic_hora)], axis=1)
    # Renombra algunas columnas y organiza el orden
    new_data.rename(
        {"MAGNITUD": "Magnitud", "PROFUNDIDAD": "Profundidad"}, axis=1, inplace=True
    )
    new_data = new_data[
        [
            "Año",
            "Mes",
            "Dia",
            "Hora",
            "Minutos",
            "Segundos",
            "Latitud",
            "Longitud",
            "Magnitud",
            "Profundidad",
        ]
    ]
    return new_data

# Llama a la función para procesar los datos
new_data = get_new_data(data)
# Guarda los datos procesados en el estado de sesión para poder utilizarlos más tarde
if "data" not in st.session_state:
    st.session_state["data"] = new_data

# Muestra los cambios realizados en los datos
st.subheader("Cambios en los datos")
st.write("Se hizo cambios al conjunto de datos para un mejor análisis.")
st.subheader("Columnas")
st.write(
    """
    - **Año**: El año en que ocurrió el sismo.
    - **Mes**: El mes en que ocurrió el sismo.
    - **Día**: El día en que ocurrió el sismo.
    - **Hora**: Hora cuando ocurrió el sismo.
    - **Minutos**: Minutos cuando ocurrió el sismo.
    - **Segundos**: Segundos cuando ocurrió el del sismo.
    - **Latitud**: Es la distancia en grados, minutos y segundos que hay con 
        respecto al paralelo principal, que es el ecuador (0º). 
        La latitud puede ser norte y sur.
    - **Longitud**: Es la distancia en grados, minutos y segundos que hay 
        con respecto al meridiano principal, que es el meridiano de Greenwich (0º).
    - **Profundidad**: Profundidad del foco sísmico por debajo de la superficie.
    - **Magnitud**: Corresponde a la cantidad de energía liberada por el sismo 
        y esta expresada en la escala de magnitud momento Mw.
"""
)
st.write(new_data) # Muestra los datos procesados

# Integrantes del grupo:
with st.sidebar:
    st.write(f"Authores : ")
    name = "- BERTIL VASTHIAN "
    last_name = "RODRIGUEZ VALDERRAMA"
    st.write(f"  {name} {last_name}")
    name = "- CARLOS ENRIQUEZ "
    last_name = "MANTILLA AGUILA"
    st.write(f"  {name} {last_name}")
    name = "- NILDA MARIBEL"
    last_name = "TURPO HUAMAN"
    st.write(f"  {name} {last_name}")
    name = "- NOEMI SALOMINA"
    last_name = "ARQUIÑO CERNA"
    st.write(f"  {name} {last_name}")
