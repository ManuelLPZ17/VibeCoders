@echo off
echo Levantando contenedores VibeCoders...
docker compose up -d

echo.
echo Esperando a que los servicios esten listos...
echo (Cassandra tarda ~60 segundos en arrancar)

:wait_mongo
docker compose exec mongo mongosh --eval "db.adminCommand('ping')" >nul 2>&1
if errorlevel 1 (
    echo   MongoDB iniciando...
    timeout /t 5 /nobreak >nul
    goto wait_mongo
)
echo   MongoDB listo.

:wait_dgraph
curl -s http://localhost:8080/health >nul 2>&1
if errorlevel 1 (
    echo   Dgraph iniciando...
    timeout /t 5 /nobreak >nul
    goto wait_dgraph
)
echo   Dgraph listo.

:wait_cassandra
docker compose exec cassandra cqlsh -e "describe keyspaces" >nul 2>&1
if errorlevel 1 (
    echo   Cassandra iniciando...
    timeout /t 10 /nobreak >nul
    goto wait_cassandra
)
echo   Cassandra listo.

echo.
echo Todos los servicios listos. Poblando bases de datos...
python populate.py

echo.
echo Listo. Corre:  python main.py
