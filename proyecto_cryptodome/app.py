# Importamos las bibliotecas requeridas
import streamlit as st
import os

# Importamos las funciones necesarias para el cifrado
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Establecemos el título de la aplicación
st.title("Cifrado con PyCry - Encriptación y Desencriptación")

# Inicializamos la variable para el texto encriptado si no existe
if "texto_encriptado" not in st.session_state:
    st.session_state.texto_encriptado = ""  # Variable para almacenar el texto encriptado

# Generamos una clave aleatoria de 16 bytes si no existe
if "clave" not in st.session_state:
    st.session_state.clave = get_random_bytes(16)

# Inicializamos la variable nonce para su uso posterior
if "nonce" not in st.session_state:
    st.session_state.nonce = None

# Inicializamos la variable tag para su uso posterior
if "tag" not in st.session_state:
    st.session_state.tag = None

# Subimos el archivo que se va a procesar
archivo = st.file_uploader("Selecciona un archivo TXT", type=["txt"], key="file_uploader_2")

# Si se ha subido un archivo, procedemos
if archivo:
    contenido = archivo.read().decode("utf-8")  # Leemos y decodificamos el contenido del archivo
    st.text_area("Contenido del archivo:", contenido, height=200)  # Mostramos el contenido en un área de texto
    st.session_state.texto_encriptado = contenido  # Almacenamos el contenido en la variable

    if st.button("Encriptar"):
        st.session_state.cifrador = AES.new(st.session_state.clave, AES.MODE_EAX)
        st.session_state.texto_encriptado = contenido.encode()
        st.session_state.cifrado, st.session_state.tag = st.session_state.cifrador.encrypt_and_digest(st.session_state.texto_encriptado)
        st.session_state.nonce = st.session_state.cifrador.nonce

        # Creamos el directorio si no existe
        if not os.path.exists("archivos"):
            os.makedirs("archivos")

        # Guardamos el texto encriptado en un archivo
        with open("archivos/encriptado.txt", "wb") as f:
            f.write(st.session_state.cifrado)
        st.markdown(f"**Texto encriptado:** `{st.session_state.cifrado}`")

    if st.button("Desencriptar"):
        if st.session_state.texto_encriptado and st.session_state.nonce and st.session_state.tag:
            cifrador_dec = AES.new(st.session_state.clave, AES.MODE_EAX, st.session_state.nonce)

            try:
                st.session_state.texto_desencriptado = cifrador_dec.decrypt(st.session_state.cifrado).decode()

                # Guardamos el texto desencriptado en un archivo
                with open("archivos/desencriptado.txt", "w") as f:
                    f.write(st.session_state.texto_desencriptado)

                st.markdown(f"**Texto desencriptado:** `{st.session_state.texto_desencriptado}`")

            except Exception as e:
                st.error("Error: El texto encriptado no es válido o la clave es incorrecta")

        else:
            st.warning("No hay texto encriptado disponible para desencriptar. Primero encripta un texto.")