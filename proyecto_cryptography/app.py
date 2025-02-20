# Importamos las bibliotecas necesarias
import streamlit as st
import os
from cryptography.fernet import Fernet

# Establecemos el título de la aplicación
st.title("Cifrado con Cryptography - Encriptación y Desencriptación")

# Inicializamos el estado de la sesión para el texto encriptado y la clave
if "texto_cifrado" not in st.session_state:
    st.session_state.texto_cifrado = ""

if "clave_secreta" not in st.session_state:
    st.session_state.clave_secreta = Fernet.generate_key()

# Subida de archivo
archivo_subido = st.file_uploader("Selecciona un archivo TXT", type=["txt"], key="file_uploader_2")

if archivo_subido:
    contenido_archivo = archivo_subido.read().decode("utf-8")  # Leemos y decodificamos el archivo en UTF-8
    st.text_area("Contenido del archivo:", contenido_archivo, height=200)  # Mostramos el contenido en un área de texto
    st.session_state.texto_cifrado = contenido_archivo
    
    if st.button("Cifrar"):
        st.session_state.cifrador = Fernet(st.session_state.clave_secreta)
        st.session_state.texto_cifrado = contenido_archivo.encode()
        st.session_state.cifrado = st.session_state.cifrador.encrypt(st.session_state.texto_cifrado)
        
        # Crear directorio si no existe
        if not os.path.exists("archivos"):
            os.makedirs("archivos")
        
        # Guardar el texto cifrado en un archivo
        with open("archivos/cifrado.txt", "wb") as f:
            f.write(st.session_state.cifrado)
        
        st.markdown(f"**Texto cifrado:** `{st.session_state.cifrado}`")
    
    if st.button("Descifrar"):
        if st.session_state.texto_cifrado:
            st.session_state.cifrador_dec = Fernet(st.session_state.clave_secreta)
            try:
                st.session_state.texto_descifrado = st.session_state.cifrador_dec.decrypt(st.session_state.cifrado).decode()
                
                # Guardar el texto descifrado en un archivo
                with open("archivos/descifrado.txt", "w") as f:
                    f.write(st.session_state.texto_descifrado)
                
                st.markdown(f"**Texto descifrado:** `{st.session_state.texto_descifrado}`")
            except Exception as e:
                st.error("Error: El texto cifrado no es válido o la clave es incorrecta")
        else:
            st.warning("No hay texto cifrado disponible para descifrar. Primero cifra un texto.")