# Cassandra

Esta carpeta contiene el modelo de datos en Cassandra.

Cassandra se utiliza para almacenar datos históricos y eventos de la plataforma, como sesiones de estudio, avance por lección, cuestionarios presentados, actividad diaria, reproducción de videos, entregas de tareas y notificaciones.

Archivos:

- schema.cql: crea el keyspace y las tablas de Cassandra
- queries.cql: incluye las consultas CQL que responden a cada requerimiento

Uso:

1. Ejecutar schema.cql para crear las tablas
2. Usar queries.cql para probar las consultas planeadas
