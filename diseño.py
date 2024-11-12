import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# URL del archivo Excel (reemplaza con tu enlace)
url = "https://tu-enlace-al-archivo.xlsx"

@st.cache_data
def load_data():
    try:
        # Hacer la solicitud HTTP para descargar el archivo
        response = requests.get(url)
        
        # Comprobar si la solicitud fue exitosa
        if response.status_code == 200:
            # Leer el archivo Excel desde la respuesta
            data_raw = pd.read_excel(BytesIO(response.content))
            st.success("Datos cargados exitosamente.")
            return data_raw
        else:
            st.error(f"Error al descargar el archivo: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None

# Cargar los datos
data = load_data()

# Mostrar los datos si se cargaron correctamente
if data is not None:
    st.dataframe(data)
else:
    st.warning("No se pudieron cargar los datos.")
