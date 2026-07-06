# 𝑳𝒂𝒃𝒐𝒓𝒂𝒕𝒐𝒓𝒊𝒐 𝑷𝒉𝒚𝒕𝒐𝒏 - 𝑮𝒓𝒖𝒑𝒐 𝑪𝟐𝟕
## 👥 Integrantes
* **Araujo Ledezma, Pilar** - Legajo: 31527
* **Perez, Bianca Belen** - Legajo: 31883
* **Sosa, Milena Tali** - Legajo:  31041

## 📚 Información Académica

**Universidad Tecnológica Nacional - Facultad Regional Resistencia**

<p align="center">
  <img width="222" height="227" alt="log-UTN 2" src="https://github.com/user-attachments/assets/4e1f2f7f-0178-444f-911a-454a80a7fc89" />
</p>

* **Cátedra:** Algoritmos y Estructuras de Datos.
* **Comisión:** C
* **Año:** 2026
  
## 📑 Descripción General
Este proyecto contará en un sistema desarrollado en Python que permite administrar la inscripción
de estudiantes a cursos o talleres. 

**Funcionalidades principales:**
- Registro de estudiantes, con validación de DNI y nombre.
- Inscripción de estudiantes a cursos, con control de cupo máximo.
- Lista de espera automática cuando un curso no tiene cupo disponible.
- Visualización de cursos y cupos disponibles en tiempo real.
- Estadísticas: total de inscriptos, total de estudiantes registrados y curso
  con mayor demanda.

El sistema utiliza estructuras condicionales, estructuras repetitivas, funciones, validaciones de datos, manejo de errores, y
acumuladores/contadores para calcular las estadísticas.

## 🗂 Metodología de trabajo y Uso de Inteligencia Artificial 
Para la organización y desarrollo de este taller, adoptamos un método de trabajo donde dividimos las tareas para optimizar los tiempos disponible antes de la fecha límite de entrega del proyecto, permitiendonos equilibrar la carga horaria y la complejidad del taller con el resto de nuestras responsabilidades académicas y personales.
 En primera instancia, optamos por diseñar una estructura básica del código, desarrollando el proceso y las funciones o procedimientos principales del algoritmo, utilizando el Pseudocódigo dictado por la cátedra. Implementamos **Inteligencia Artificial** como herramienta de asistencia para traducir nuestra lógica base al lenguaje Python. Utilizando el material teórico brindado por la cátedra, pudimos verificar la correlación directa y la equivalencia entre las estructuras de control en pseudocódigo y su sintaxis correspondiente en Python. Y, por último, mediante el diseño de prompts específicos y detallados, solicitamos a la IA la detección de posibles errores de lógica, y la propuesta de optimización y ámpliación del código.

### _Nuestro Desarrollo del Algoritmo En Pseudocódigo_

Acción SistemadeInscripciones es
  PROCEDIMIENTO 1: MOSTRAR CURSOS
   
    PROCEDIMIENTO mostrar_cursos()
        Curso: caracter
        Cupo: caracter
        
        Escribir ("LISTA DE CURSOS DISPONIBLES")
                ABRIR(cursos.txt, leer)
        
        MIENTRAS NFDA (cursos.txt) HACER
            // Leemos el nombre del curso
            Leer (cursos.txt, curso)
            // Leemos el cupo que está en la siguiente línea
            Leer (cursos.txt, cupo)
            
            SI curso <> " " ENTONCES
                ESCRIBIR (“- ", curso, ". Cupos disponibles:", cupo)
            FIN_SI
        FIN_MIENTRAS
        
        CERRAR(cursos.txt)
    FIN_PROCEDIMIENTO


  FUNCION 2: Buscar Cupo
   
     FUNCION obtener_cupo_maximo(curso_buscado : Caracter) : Entero
      Curso_actual: Caracter
      Cupo_actual_str: Caracter
      Encontrado: Booleano // bandera de control
    
      obtener_cupo_maximo := 0
      Encontrado := Falso 
    
      ABRIR(cursos.txt, leer)
    
      Mientras NFDA (cursos.txt) Y (Encontrado = Falso) hacer
        LEER(cursos.txt, curso_actual)
        LEER(cursos.txt, cupo_actual_str)
        
        SI curso_actual = curso_buscado ENTONCES
            obtener_cupo_maximo := CONVERTIR_A_ENTERO(cupo_actual_str)
            Encontrado := Verdadero // ¡Lo encontramos! Esto frena el bucle en la próxima vuelta
        FIN_SI
     FIN_MIENTRAS
    
     CERRAR(cursos.txt)
    FIN_FUNCION


PROCEDIMIENTO 3: REGISTRAR ALUMNO
    
    PROCEDIMIENTO registrar_inscripcion(alumno : caracter, curso : caracter)
        // Abrimos el archivo 
               ABRIR(inscripciones.txt) 
        
        // Guardamos los datos
        Escribir(inscripciones.txt, alumno)
        Escribir(inscripciones.txt, curso)
        
        CERRAR(inscripciones.txt)
        ESCRIBIR ("Estudiante registrado con éxito.")
    FIN_PROCEDIMIENTO



PROCEDIMIENTO 4: ESTADÍSTICAS POR CARRERA

     PROCEDIMIENTO mostrar_estadisticas()
       curso_catalogo : Caracter
       cupo_catalogo : Caracter
       alumno_inscripto : Caracter
       curso_inscripto : Caracter
       contador_por_curso : Entero
    
      ESCRIBIR ("ESTADÍSTICAS DE INSCRITOS POR CARRERA")
    
    // 1. Abrimos el archivo de cursos para saber qué carreras existen
    ABRIR(cursos.txt, LEER)
    
     MIENTRAS NO NFDA (cursos.txt) HACER
        LEER(cursos.txt, curso_catalogo)
        LEER(cursos.txt, cupo_catalogo)
        
        SI curso_catalogo <> " " ENTONCES
            // Cada vez que cambiamos de curso, el contador vuelve a 0
            contador_por_curso := 0
            
            // 2. Abrimos el archivo de inscripciones para contar los alumnos de este curso
            ABRIR(inscripciones.txt, LEER)
            
            MIENTRAS NO NFDA(inscripciones.txt) HACER
                LEER(inscripciones.txt, alumno_inscripto)
                LEER(inscripciones.txt, curso_inscripto)
                
                // Si el curso del alumno coincide con el curso que estoy analizando, sumo 1
                SI curso_inscripto = curso_catalogo ENTONCES
                    contador_por_curso := contador_por_curso + 1
                FIN_SI
            FIN_MIENTRAS
            
            // Cerramos inscripciones para que en la próxima vuelta se pueda leer desde el principio
            CERRAR(inscripciones.txt)
            
            // Mostramos el resultado en pantalla para esta carrera
            ESCRIBIR ("- ", curso_catalogo, ": ", contador_por_curso, " inscriptos.")
        FIN_SI
     FIN_MIENTRAS
    
     CERRAR("cursos.txt")
     FIN_PROCEDIMIENTO

PROCESO PRINCIPAL 
 
    PROCEDIMIENTO iniciar_programa()
        nombre_alumno : Caracter
        curso_elegido : Caracter
        cupo_disponible : Entero
        
        ESCRIBIR ("BIENVENIDOS")
        mostrar_cursos() // Muestra la lista
        
        ESCRIBIR "Ingrese Nombre y Apellido del alumno:"
        LEER (nombre_alumno)
        
        ESCRIBIR ("Ingrese el nombre del curso de manera exacta:")
        LEER (curso_elegido)
        
        // Buscamos el cupo
        cupo_disponible := obtener_cupo_maximo(curso_elegido)
        
              SI cupo_disponible > 0 ENTONCES
                  registrar_inscripcion(nombre_alumno, curso_elegido)
             sino
                  ESCRIBIR "El curso ingresado no existe."
        FIN_SI
        
        mostrar_estadisticas()
    FIN_ACCION







