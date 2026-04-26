# Plataforma de Educación en Línea - VibeCoders

## Integrantes
- Manuel Alfonso Lopez Ponce De Leon — 753353  
- Carlos Emiliano Olmedo Navarro — 754232  
- Jorge Alberto Rivera Clemente — 760161  
- Diego Saúl Castillo Fuentes — 754035  

---

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de una **Plataforma de Educación en Línea**, la cual permite:

- A instructores crear y publicar cursos  
- A estudiantes inscribirse en cursos  
- Consumir contenido educativo  
- Dar seguimiento a su progreso académico  

El sistema utiliza **tres bases de datos NoSQL** para aprovechar sus ventajas en distintos escenarios:

- **MongoDB** → almacenamiento de datos estructurados tipo documento (usuarios, cursos, contenido)  
- **Dgraph** → manejo de relaciones complejas entre entidades (alumnos, cursos, tareas, etc.)  
- **Cassandra** → registro de actividad y eventos de alto volumen (progreso, sesiones, intentos)  

---

## Objetivo del Proyecto

Diseñar e implementar un sistema distribuido que utilice múltiples modelos de bases de datos NoSQL, demostrando cómo cada tecnología resuelve diferentes necesidades del sistema de manera eficiente.

---

## Flujo de Trabajo (General)

1. **Inserción de datos**
   - Los datos se generan o cargan desde la carpeta `/data`
   - Se insertan en cada base de datos según su modelo:
     - MongoDB → documentos
     - Cassandra → tablas orientadas a consultas
     - Dgraph → nodos y relaciones

2. **Procesamiento**
   - Cada base de datos maneja una parte específica del sistema:
     - MongoDB → información principal del sistema
     - Dgraph → relaciones entre entidades
     - Cassandra → eventos y métricas

3. **Consultas**
   - El archivo `main.py` mostrará un menú con las consultas planeadas
   - Las consultas permitirán:
     - Ver cursos
     - Consultar progreso
     - Analizar actividad
     - Explorar relaciones

---

## Estructura del Proyecto

VibeCoders/
├── Cassandra/
├── Mongo/
├── Dgraph/
├── data/
├── connect.py
├── populate.py
├── main.py
└── README.md