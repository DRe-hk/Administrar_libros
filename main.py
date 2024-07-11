import streamlit as st
import pandas as pd

class Libro:
    def __init__(self, titulo, autor, anio, genero, isbn):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.genero = genero
        self.isbn = isbn

    def __str__(self):
        return f"Titulo: {self.titulo}, Autor: {self.autor}, Año: {self.anio}, Genero: {self.genero}, ISBN: {self.isbn}"

class Inventario:
    def __init__(self):
        self.df = pd.DataFrame(columns=['Titulo', 'Autor', 'Año', 'Genero', 'ISBN'])

    def agregar_libro(self, libro):
        nuevo_libro = pd.DataFrame([[libro.titulo, libro.autor, libro.anio, libro.genero, libro.isbn]],
                                   columns=['Titulo', 'Autor', 'Año', 'Genero', 'ISBN'])
        self.df = pd.concat([self.df, nuevo_libro], ignore_index=True)

    def eliminar_libro(self, isbn):
        self.df = self.df[self.df['ISBN'] != isbn]

    def buscar_libro(self, titulo):
        return self.df[self.df['Titulo'].str.lower() == titulo.lower()]

    def listar_libros(self):
        return self.df

    def actualizar_libro(self, titulo, nuevo_titulo, nuevo_autor, nuevo_anio, nuevo_genero, nuevo_isbn):
        self.df.loc[self.df['Titulo'].str.lower() == titulo.lower(), ['Titulo', 'Autor', 'Año', 'Genero', 'ISBN']] = [nuevo_titulo, nuevo_autor, nuevo_anio, nuevo_genero, nuevo_isbn]

    def guardar_csv(self, nombre_archivo):
        self.df.to_csv(nombre_archivo, index=False)

def validar_entero(input_str, nombre_campo):
    try:
        valor = int(input_str)
        return valor
    except ValueError:
        st.error(f"Entrada inválida para {nombre_campo}. Debe ser un número entero.")
        return None

if 'inventario' not in st.session_state:
    st.session_state.inventario = Inventario()

def main():
    st.sidebar.title("Menú de opciones")
    opciones = ["Agregar libro", "Eliminar libro", "Buscar libro", "Listar libros", "Actualizar libro", "Guardar en CSV"]
    opcion = st.sidebar.selectbox("Elija una opción:", opciones)

    inventario = st.session_state.inventario

    if opcion == "Agregar libro":
        st.title("Agregar Libro")
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        anio = st.text_input("Año")
        genero = st.text_input("Género")
        isbn = st.text_input("ISBN")
        if st.button("Agregar"):
            anio_valido = validar_entero(anio, "Año")
            if anio_valido is not None:
                libro = Libro(titulo, autor, anio_valido, genero, isbn)
                inventario.agregar_libro(libro)
                st.session_state.inventario = inventario
                st.success("Libro agregado.")

    elif opcion == "Eliminar libro":
        st.title("Eliminar Libro")
        isbn = st.text_input("ISBN del libro a eliminar")
        if st.button("Eliminar"):
            inventario.eliminar_libro(isbn)
            st.session_state.inventario = inventario
            st.success("Intento de eliminación completado.")

    elif opcion == "Buscar libro":
        st.title("Buscar Libro")
        titulo = st.text_input("Título del libro a buscar")
        if st.button("Buscar"):
            resultado = inventario.buscar_libro(titulo)
            if not resultado.empty:
                st.write(resultado)
            else:
                st.warning("Libro no encontrado.")

    elif opcion == "Listar libros":
        st.title("Listado de Libros")
        libros = inventario.listar_libros()
        if libros.empty:
            st.warning("No hay libros en el inventario.")
        else:
            st.dataframe(libros)

    elif opcion == "Actualizar libro":
        st.title("Actualizar Libro")
        titulo = st.text_input("Título del libro a actualizar")
        if st.button("Buscar"):
            libro = inventario.buscar_libro(titulo)
            if not libro.empty:
                st.write(libro)
                nuevo_titulo = st.text_input("Nuevo título")
                nuevo_autor = st.text_input("Nuevo autor")
                nuevo_anio = st.text_input("Nuevo año")
                nuevo_genero = st.text_input("Nuevo género")
                nuevo_isbn = st.text_input("Nuevo ISBN")
                if st.button("Actualizar"):
                    nuevo_anio_valido = validar_entero(nuevo_anio, "Nuevo año")
                    if nuevo_anio_valido is not None:
                        inventario.actualizar_libro(titulo, nuevo_titulo, nuevo_autor, nuevo_anio_valido, nuevo_genero, nuevo_isbn)
                        st.session_state.inventario = inventario
                        st.success("Libro actualizado.")
            else:
                st.warning("Libro no encontrado.")

    elif opcion == "Guardar en CSV":
        st.title("Guardar en CSV")
        nombre_archivo = st.text_input("Nombre del archivo (con .csv)")
        if st.button("Guardar"):
            if nombre_archivo:
                inventario.guardar_csv(nombre_archivo)
                st.success("Inventario guardado en CSV.")
                with open(nombre_archivo, 'rb') as file:
                    st.download_button(label="Descargar CSV", data=file, file_name=nombre_archivo, mime='text/csv')
            else:
                st.error("Por favor, ingrese un nombre de archivo.")

if __name__ == "__main__":
    main()
