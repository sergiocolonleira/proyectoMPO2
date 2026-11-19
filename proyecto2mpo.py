import os
from datetime import datetime


def mostrar_menu():
    print("\n===== GESTOR DE ARCHIVOS =====")
    print("Directorio actual:", os.getcwd())
    print("1. Listar contenido del directorio actual")
    print("2. Crear un nuevo directorio")
    print("3. Crear un archivo de texto")
    print("4. Escribir texto en un archivo existente")
    print("5. Eliminar un archivo o directorio")
    print("6. Mostrar información del archivo")
    print("7. Salir")


def pedir_nombre():
    nombre = input("Nombre del archivo o carpeta: ").strip()

    if not nombre or nombre in (".", "..") or "/" in nombre or "\\" in nombre:
        print("Error: introduce un nombre válido, sin rutas ni separadores.")
        return None

    return nombre


def listar_contenido():
    try:
        elementos = os.listdir()
        if not elementos:
            print("El directorio está vacío.")
            return

        for nombre in sorted(elementos):
            if os.path.isdir(nombre):
                tipo = "Carpeta"
            else:
                tipo = "Archivo"
            print(f"{tipo}: {nombre}")
    except OSError as error:
        print("No se pudo listar el contenido:", error)


def crear_directorio():
    nombre = pedir_nombre()
    if nombre is None:
        return

    try:
        os.mkdir(nombre)
        print("Carpeta creada correctamente.")
    except FileExistsError:
        print("Error: ya existe un archivo o carpeta con ese nombre.")
    except OSError as error:
        print("No se pudo crear la carpeta:", error)


def crear_archivo():
    nombre = pedir_nombre()
    if nombre is None:
        return

    if not nombre.lower().endswith(".txt"):
        nombre += ".txt"

    contenido = input("Escribe el contenido inicial: ")

    try:
        # El modo x crea el archivo solo si todavía no existe.
        with open(nombre, "x", encoding="utf-8") as archivo:
            archivo.write(contenido)
        print("Archivo creado correctamente:", nombre)
    except FileExistsError:
        print("Error: ya existe un archivo o carpeta con ese nombre.")
    except OSError as error:
        print("No se pudo crear el archivo:", error)


def elegir_elemento(elementos):
    if not elementos:
        print("No hay elementos disponibles.")
        return None

    for numero, nombre in enumerate(elementos, 1):
        if os.path.isdir(nombre):
            tipo = "Carpeta"
        else:
            tipo = "Archivo"
        print(f"{numero}. [{tipo}] {nombre}")

    opcion = input("Introduce el número (0 para cancelar): ").strip()
    if not opcion.isdigit():
        print("Error: introduce un número válido.")
        return None

    numero = int(opcion)
    if numero == 0:
        print("Operación cancelada.")
        return None
    if numero < 1 or numero > len(elementos):
        print("Error: ese número no está en la lista.")
        return None

    return elementos[numero - 1]


def escribir_en_archivo():
    try:
        archivos = sorted(
            nombre for nombre in os.listdir()
            if os.path.isfile(nombre) and nombre.lower().endswith(".txt")
        )
        print("\nArchivos de texto disponibles:")
        nombre = elegir_elemento(archivos)
        if nombre is None:
            return

        texto = input("Texto que deseas añadir: ")
        with open(nombre, "a", encoding="utf-8") as archivo:
            archivo.write("\n" + texto)
        print("Texto añadido correctamente.")
    except OSError as error:
        print("No se pudo escribir en el archivo:", error)


def eliminar_elemento():
    try:
        elementos = sorted(os.listdir())
        print("\nArchivos y carpetas disponibles:")
        nombre = elegir_elemento(elementos)
        if nombre is None:
            return

        confirmacion = input(f"¿Seguro que deseas eliminar '{nombre}'? (s/n): ").strip().lower()
        if confirmacion != "s":
            print("Eliminación cancelada.")
            return

        if os.path.isdir(nombre):
            os.rmdir(nombre)
        else:
            os.remove(nombre)
        print("Elemento eliminado correctamente.")
    except OSError as error:
        print("No se pudo eliminar (las carpetas deben estar vacías):", error)


def mostrar_informacion():
    nombre = pedir_nombre()
    if nombre is None:
        return

    try:
        if os.path.isdir(nombre):
            tipo = "Carpeta"
        elif os.path.isfile(nombre):
            tipo = "Archivo"
        else:
            print("Error: el archivo o carpeta no existe.")
            return

        tamano = os.path.getsize(nombre)
        fecha = os.path.getmtime(nombre)
        fecha_formateada = datetime.fromtimestamp(fecha).strftime("%d/%m/%Y %H:%M:%S")

        print("Nombre:", nombre)
        print("Tipo:", tipo)
        print("Tamaño:", tamano, "bytes")
        print("Última modificación:", fecha_formateada)
    except OSError as error:
        print("No se pudo obtener la información:", error)


def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            listar_contenido()
        elif opcion == "2":
            crear_directorio()
        elif opcion == "3":
            crear_archivo()
        elif opcion == "4":
            escribir_en_archivo()
        elif opcion == "5":
            eliminar_elemento()
        elif opcion == "6":
            mostrar_informacion()
        elif opcion == "7":
            print("Hasta pronto.")
            break
        else:
            print("Opción no válida. Elige un número del 1 al 7.")


if __name__ == "__main__":
    main()
