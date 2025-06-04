import sqlite3
import psycopg2

# Conexión a SQLite
sqlite_conn = sqlite3.connect("usuarios.db")
sqlite_cursor = sqlite_conn.cursor()

# Conexión a PostgreSQL en Render
pg_conn = psycopg2.connect(
    dbname="mod_aut_pjic_db",
    user="mod_aut_pjic_db_user",
    password="WoHiB1NxcR1lGle8eH2Kho1PY72AQetK",
    host="dpg-d1067vu3jp1c739lka00-a.oregon-postgres.render.com",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Crear tabla 'usuarios' en PostgreSQL si no existe
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario TEXT UNIQUE,
    clave_hash TEXT,
    dependencia TEXT,
    es_superusuario INTEGER
);
""")

# Extraer datos desde SQLite
sqlite_cursor.execute("SELECT usuario, clave_hash, dependencia, es_superusuario FROM usuarios")
usuarios = sqlite_cursor.fetchall()

# Insertar en PostgreSQL
for fila in usuarios:
    pg_cursor.execute("""
        INSERT INTO usuarios (usuario, clave_hash, dependencia, es_superusuario)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (usuario) DO NOTHING
    """, fila)

pg_conn.commit()

print(f"✅ Usuarios migrados exitosamente: {len(usuarios)} registros.")

# Cierre de conexiones
sqlite_conn.close()
pg_cursor.close()
pg_conn.close()