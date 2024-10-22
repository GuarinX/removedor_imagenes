import os  # Importamos el módulo os para manejar operaciones del sistema, como la creación de carpetas.
from PIL import Image  # Importamos la clase Image de la biblioteca PIL para trabajar con imágenes.
from rembg import remove  # Importamos la función remove del paquete rembg para eliminar el fondo de las imágenes.
import streamlit as st  # Importamos Streamlit para crear la interfaz web interactiva.

# Función para guardar el archivo subido por el usuario
def save_uploaded_file(upload_file):
    upload_dir = "uploads"  # Definimos la carpeta donde se guardarán las imágenes subidas.
    if not os.path.exists(upload_dir):  # Si la carpeta no existe, la creamos.
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, upload_file.name)  # Definimos la ruta completa del archivo.
    with open(file_path, "wb") as f:  # Guardamos el archivo en modo binario.
        f.write(upload_file.getbuffer())  # Escribimos el contenido del archivo.
    return file_path  # Devolvemos la ruta del archivo guardado.

# Función para eliminar el fondo de una imagen
def run_background_remove(input_img_file):
    input_img_path = save_uploaded_file(input_img_file)  # Guardamos el archivo subido y obtenemos su ruta.
    output_img_path = input_img_path.replace('.', '_rmbg.').replace('jpg', 'png').replace('jpeg', 'png')  # Generamos el nombre para el archivo procesado.
    try:
        image = Image.open(input_img_path)  # Abrimos la imagen utilizando PIL.
        output = remove(image)  # Eliminamos el fondo de la imagen utilizando la función remove.
        output.save(output_img_path, 'PNG')  # Guardamos la imagen procesada con el fondo eliminado.

        # Creamos dos columnas para mostrar las imágenes lado a lado en la interfaz.
        col1, col2 = st.columns(2)

        with col1:  # Columna para la imagen original.
            st.header("Antes")  # Encabezado para la imagen original.
            st.image(input_img_path, caption="Imagen Original")  # Mostramos la imagen original.
            with open(input_img_path, "rb") as image_file:  # Preparamos la descarga de la imagen original.
                st.download_button(
                    label="Descargar Imagen Original",
                    data=image_file,
                    file_name=os.path.basename(input_img_path),
                    mime="image/jpeg"
                )

        with col2:  # Columna para la imagen con el fondo removido.
            st.header("Después")  # Encabezado para la imagen procesada.
            st.image(output_img_path, caption="Imagen con fondo removido")  # Mostramos la imagen con fondo eliminado.
            with open(output_img_path, "rb") as image_file:  # Preparamos la descarga de la imagen procesada.
                st.download_button(
                    label="Descargar Imagen procesada",
                    data=image_file,
                    file_name=os.path.basename(output_img_path),
                    mime="image/png"
                )

        st.success("¡Fondo removido con éxito!")  # Mensaje de éxito si todo el proceso funciona correctamente.
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")  # Mensaje de error en caso de que ocurra un problema.

# Función principal de la aplicación
def main():
    st.title("Removedor de fondos")  # Título de la aplicación.
    uploaded_file = st.file_uploader("Elige un archivo de imagen", type=["jpg", "jpeg", "png"])  # Componente para que el usuario suba una imagen.
    if uploaded_file is not None:  # Si el usuario ha subido una imagen, llamamos a la función para remover el fondo.
        run_background_remove(uploaded_file)

# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()  # Ejecutamos la función principal si el script se ejecuta directamente.