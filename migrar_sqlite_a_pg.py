import sqlite3
import psycopg2

# Ruta a tu base de datos SQLite
sqlite_conn = sqlite3.connect("usuarios.db")
sqlite_cursor = sqlite_conn.cursor()

# Conexión PostgreSQL
pg_conn = psycopg2.connect(
    dbname="mod_aut_pjic_db",
    user="mod_aut_pjic_db_user",
    password="WoHiB1NxcR1lGle8eH2Kho1PY72AQetK",
    host="dpg-d1067vu3jp1c739lka00-a.oregon-postgres.render.com",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Crear tabla si no existe en PostgreSQL
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS credenciales_gt (
    id SERIAL PRIMARY KEY,
    usuario_sistema TEXT,
    gt_usuario TEXT,
    gt_clave_encriptada TEXT,
    dependencia TEXT
);
""")

# Extraer los datos de SQLite
sqlite_cursor.execute("SELECT usuario_sistema, gt_usuario, gt_clave_encriptada, dependencia FROM credenciales_gt")
registros = sqlite_cursor.fetchall()

# Insertar en PostgreSQL
for fila in registros:
    pg_cursor.execute("""
        INSERT INTO credenciales_gt (usuario_sistema, gt_usuario, gt_clave_encriptada, dependencia)
        VALUES (%s, %s, %s, %s)
    """, fila)

pg_conn.commit()
print(f"✅ Total registros migrados: {len(registros)}")
print("🚀 Datos migrados exitosamente.")

# Cerrar conexiones
sqlite_conn.close()
pg_cursor.close()
pg_conn.close()