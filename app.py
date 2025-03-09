# Dependencias
import streamlit as st
import requests
from datetime import datetime

# Función para obtener la imagen del día
def img_de_hoy(api_key):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: No se pudo obtener la imagen del día.")
        return None

# Función para obtener imagen del Rover Curiosity
def fotos_mars_rover(api_key, sol=1000):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: No se pudieron obtener las imágenes del Rover.")
        return None

# Función para obtener asteroides cercanos
def asteroides_cercanos(api_key):
    today = datetime.today().strftime("%Y-%m-%d")
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: No se pudieron obtener los asteroides cercanos.")
        return None

# Título
st.title("Exploración Espacial con la NASA 🚀")

# Menú
menu = ["Exploración Espacial con la NASA", 
        "Imagen del Día", 
        "Buscar Imagen por Fecha", 
        "Asteroides Cercanos", 
        "Imágenes Mars Rover"]

# Selector de menú
option = st.sidebar.selectbox("Selecciona una opción", menu)

if option == "Exploración Espacial con la NASA":
    api_key = st.text_input("Ingresa tu API Key de la NASA:", type="password")
    if api_key:
        st.session_state.api_key = api_key
    if not api_key:
        st.warning("Por favor, ingresa una API Key para continuar.")
        st.stop()
    
    st.markdown("""
        # Bienvenidos a la aplicación de exploración espacial usando la API de la NASA. 
        Aquí podrás acceder a datos sobre el espacio y Marte. 
        Explora las imágenes más recientes del espacio, observa los asteroides cercanos a la Tierra, 
        y sumérgete en las fotos tomadas por los rovers de la NASA en Marte.

        En esta aplicación puedes:
        - Ver la **Imagen del Día** del espacio.
        - Buscar imágenes del espacio por **fecha**.
        - Conocer los **asteroides cercanos** a la Tierra.
        - Ver imágenes tomadas por los **rovers de Marte**.
    """)

elif option in ["Imagen del Día", "Buscar Imagen por Fecha", "Asteroides Cercanos", "Imágenes Mars Rover"]:
    if "api_key" not in st.session_state:
        st.error("Debes ingresar tu API Key en la primera sección antes de continuar.")
        st.stop()
    api_key = st.session_state.api_key

    if option == "Imagen del Día":
        apod_data = img_de_hoy(api_key)
        if apod_data:
            st.image(apod_data['url'], caption=apod_data['title'], use_column_width=True)
            st.write(apod_data['explanation'])

    elif option == "Buscar Imagen por Fecha":
        date = st.date_input("Selecciona la fecha (YYYY-MM-DD)", datetime.today())
        date_str = date.strftime("%Y-%m-%d")
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date_str}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'url' in data:
                st.image(data['url'], caption=data['title'], use_column_width=True)
                st.write(data['explanation'])
            else:
                st.write("No se encontró imagen para esa fecha.")
        else:
            st.error("Error al obtener la imagen para esa fecha.")

    elif option == "Asteroides Cercanos":
        data = asteroides_cercanos(api_key)
        if data:
            today = datetime.today().strftime("%Y-%m-%d")
            if today in data['near_earth_objects']:
                st.write(f"Fecha: {today}")
                for asteroid in data['near_earth_objects'][today]:
                    st.write(f"Nombre: {asteroid['name']}")
                    st.write(f"Distancia: {asteroid['close_approach_data'][0]['miss_distance']['kilometers']} km")
                    st.write(f"Tamaño: {asteroid['estimated_diameter']['meters']['estimated_diameter_max']} metros")
                    st.write("-" * 50)
            else:
                st.write("No hay datos de asteroides para hoy.")

    elif option == "Imágenes Mars Rover":
        sol = st.number_input("Sol (día de la misión):", min_value=0, value=1000)
        data = fotos_mars_rover(api_key, sol)
        if data:
            for photo in data['photos']:
                st.image(photo['img_src'], caption=f"Rover Curiosity - Sol {sol}", use_column_width=True)
