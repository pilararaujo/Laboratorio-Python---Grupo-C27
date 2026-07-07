"""
Sistema de Gestión de Inscripciones - Academia
Traducción a Python del pseudocódigo original.
"""
from collections import Counter # cambio: se importó counter para leer el archivo de inscripciones de una sola vez (optimización) 
import os

ARCHIVO_CURSOS = "cursos.txt"
ARCHIVO_INSCRIPCIONES = "inscripciones.txt"
ARCHIVO_ESPERA = "espera.txt"

CUPO_INICIAL = 10
CURSOS_INICIALES = [
    "Programacion",
    "Diseno Grafico",
    "Marketing Digital",
    "Contabilidad",
    "Ingles",
    "Redes y Soporte Tecnico"
]

def leer_archivo_seguro(ruta): #agregamos esta función para leer archivos de manera segura y evitar errores si el archivo no existe.
    """Lee un archivo de forma segura devolviendo sus líneas limpias."""
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return [linea.strip() for linea in archivo if linea.strip()]
    except PermissionError:
        print(f"Error: El archivo {ruta} está abierto en otro programa.")
        return []
    
def inicializar_cursos():
    """Crea cursos.txt con los 6 cursos y cupo=10 SOLO si el archivo no existe aun.
    (El pseudocodigo original nunca creaba este archivo, asumia que ya existia)."""
    if not os.path.exists(ARCHIVO_CURSOS):
        try: #cambio: se agrega un try para manejar errores de escritura en el archivo 
            with open(ARCHIVO_CURSOS, "w", encoding="utf-8") as archivo:
              for curso in CURSOS_INICIALES:
                archivo.write(curso + "\n")
                archivo.write(str(CUPO_INICIAL) + "\n")
        except PermissionError: #cambio: se agrega un except para manejar errores de permisos de escritura en el archivo 
            print("Error de permisos al crear el catálogo de cursos. Asegurese de tener permisos de escritura en el directorio.")

def mostrar_cursos():
    """PROCEDIMIENTO 1: Muestra la lista de cursos disponibles con su cupo maximo."""
    print("\nLISTA DE CURSOS DISPONIBLES")
    lineas = leer_archivo_seguro(ARCHIVO_CURSOS)  # Cambio: Usa lectura segura -> Evita fallos si el archivo no existe o está bloqueado

    # cambio: Se usó zip(): Recorre de a pares de forma limpia y moderna sin usar índices manuales i e i+1 (Evita IndexError)
    for curso, cupo in zip(lineas[0::2], lineas[1::2]):
        print(f"- {curso}. Cupos disponibles: {cupo}")
    

def obtener_cupo_maximo(curso_buscado):
    """FUNCION 2: Devuelve el cupo MAXIMO original de un curso (segun cursos.txt).
    Devuelve 0 si el curso no existe en el catalogo."""
    lineas = leer_archivo_seguro(ARCHIVO_CURSOS) # CAMBIO: Se usa la función de lectura segura para evitar errores si el archivo no existe o está bloqueado 
    # CAMBIO: Se usó zip(): Recorre el catálogo de forma segura emparejando Curso y Cupo
    for curso_actual, cupo_actual_str in zip(lineas[0::2], lineas[1::2]):
        # CAMBIO: .casefold(): Compara ignorando mayúsculas/minúsculas ("Programacion" == "programacion")
        if curso_actual.casefold() == curso_buscado.casefold():
            try:
                return int(cupo_actual_str)  # CAMBIO: try/except -> Evita ValueError si el archivo fue editado con texto en vez de número
            except ValueError:
                return 0
    return 0

def obtener_todas_las_inscripciones():
    """NUEVA FUNCIÓN: Usa Counter: Abre inscripciones.txt UNA SOLA VEZ y cuenta todo. Reemplaza el bucle ineficiente O(N)."""
    lineas = leer_archivo_seguro(ARCHIVO_INSCRIPCIONES)
    # CAMBIO: Toma las líneas impares (cursos) asociadas a cada inscripción
    cursos_inscriptos = [lineas[i].casefold() for i in range(1, len(lineas), 2)]
    return Counter(cursos_inscriptos)  # CAMBIO: Devuelve un diccionario contador eficiente (Ej: {"programacion": 3, "ingles": 1})

#quitamos la función contar_inscriptos y la reemplazamos por las funciones obtener_todas_las_inscripciones y alumno_ya_inscripto, que son más eficientes y limpias. 
def obtener_todas_las_inscripciones():
    """NUEVA FUNCIÓN: Usa Counter: Abre inscripciones.txt UNA SOLA VEZ y cuenta todo. Reemplaza el bucle ineficiente O(N)."""
    lineas = leer_archivo_seguro(ARCHIVO_INSCRIPCIONES)
    # CAMBIO: Toma las líneas impares (cursos) asociadas a cada inscripción
    cursos_inscriptos = [lineas[i].casefold() for i in range(1, len(lineas), 2)]
    return Counter(cursos_inscriptos)  # CAMBIO: Devuelve un diccionario contador eficiente (Ej: {"programacion": 3, "ingles": 1})


def alumno_ya_inscripto(alumno_buscado, curso_buscado):
    """NUEVA FUNCIÓN: Regla de negocio: Valida si la combinación Alumno-Curso ya existe para evitar inscripciones duplicadas."""
    lineas = leer_archivo_seguro(ARCHIVO_INSCRIPCIONES)
    for alumno, curso in zip(lineas[0::2], lineas[1::2]):
        # CAMBIO: casefold() en ambos datos -> Evita que "Juan" se anote dos veces por llamarse "juan" o "JUAN"
        if alumno.casefold() == alumno_buscado.casefold() and curso.casefold() == curso_buscado.casefold():
            return True
    return False


def registrar_inscripcion(alumno, curso):
    """PROCEDIMIENTO 3: Guarda al alumno en inscripciones.txt.
    Usamos modo "a" (append = agregar) para sumar al final del archivo
    sin borrar a los alumnos que ya estaban registrados."""
    try: #cambio: se agregar try/except par amanejar errores de escritura
        with open(ARCHIVO_INSCRIPCIONES, "a", encoding="utf-8") as archivo:
          archivo.write(alumno + "\n")
          archivo.write(curso + "\n")
        print("Estudiante registrado con exito.")
    except PermissionError:
        print("No se pudo registrar la inscripción debido a un error de permisos.")


def registrar_espera(alumno, curso):
    """NUEVO PROCEDIMIENTO (faltaba por completo en el pseudocodigo original).
    Guarda al alumno en espera.txt cuando el curso elegido ya no tiene cupos."""
    try: # cambio: se agregar try/except par amanejar errores de escritura
        with open(ARCHIVO_ESPERA, "a", encoding="utf-8") as archivo:
          archivo.write(alumno + "\n")
          archivo.write(curso + "\n")

        print("El curso esta completo. El alumno fue agregado a la lista de espera.")
    except PermissionError:
        print("No se pudo registrar la inscripción en espera debido a un error de permisos.")

def mostrar_estadisticas():
    """PROCEDIMIENTO 4: Muestra cuantos alumnos estan inscriptos en cada curso."""
    print("\nESTADISTICAS DE INSCRITOS POR CARRERA")
lineas_cursos = leer_archivo_seguro(ARCHIVO_CURSOS)
conteo_total = obtener_todas_las_inscripciones()  # CAMBIO: Llama a la optimización con Counter: Cero lecturas repetidas de archivo
#quitamos with 
for curso_catalogo in lineas_cursos[0::2]:
        # CAMBIO: Busca directamente en el mapa de Counter usando minúsculas -> Rápido y seguro
        contador_por_curso = conteo_total[curso_catalogo.casefold()]
        print(f"- {curso_catalogo}: {contador_por_curso} inscriptos.")


def iniciar_programa():
    """PROCESO PRINCIPAL: controla el flujo. Se agrego un bucle WHILE para poder
    inscribir a VARIOS alumnos (el pseudocodigo original solo permitia uno y terminaba)."""
    inicializar_cursos()  # nos aseguramos de que cursos.txt exista con los 6 cursos

    print("BIENVENIDOS")

    while True:
        mostrar_cursos()
        #cambio: bloque de validacion para que el nombre del alumno no sea vacío y no se pueda inscribir un alumno sin nombre.
        nombre_alumno = " "
        while not nombre_alumno:
          nombre_alumno = input("\nIngrese Nombre y Apellido del alumno (o 'salir' para terminar): ").strip()
          if nombre_alumno.lower() == "salir":
            break
          if nombre_alumno.lower() == "salir":
            break
# cambio: Bucle de validación: Impide que el curso ingresado sea un texto en blanco
        curso_elegido = ""
        while not curso_elegido:
            curso_elegido = input("Ingrese el nombre del curso de manera exacta: ").strip()

        # Cambio: Validación de Duplicados : Aplica la nueva regla de negocio antes de evaluar cupos
        if alumno_ya_inscripto(nombre_alumno, curso_elegido):
            print("Error: Este estudiante ya se encuentra inscripto en este curso.")
            continue

        cupo_maximo = obtener_cupo_maximo(curso_elegido)

        if cupo_maximo == 0:
            
            print("El curso ingresado no existe.")
        else:
            # Cambio: El conteo ahora usa la clave normalizada en minúsculas del Counter optimizado
            inscriptos_actuales = obtener_todas_las_inscripciones()[curso_elegido.casefold()]
            cupo_real_disponible = cupo_maximo - inscriptos_actuales

            if cupo_real_disponible > 0:
                registrar_inscripcion(nombre_alumno, curso_elegido)
            else:
                registrar_espera(nombre_alumno, curso_elegido)

    mostrar_estadisticas()


if __name__ == "__main__":
    iniciar_programa()
     