import psycopg2

# Conexión PostgreSQL (Render)
conn = psycopg2.connect(
    dbname="mod_aut_pjic_db",
    user="mod_aut_pjic_db_user",
    password="WoHiB1NxcR1lGle8eH2Kho1PY72AQetK",
    host="dpg-d1067vu3jp1c739lka00-a.oregon-postgres.render.com",
    port="5432"
)

cursor = conn.cursor()

print("📋 Tabla usuarios:")
cursor.execute("SELECT id, usuario, dependencia, es_superusuario FROM usuarios")
for fila in cursor.fetchall():
    print(fila)

print("\n🔐 Tabla credenciales_gt:")
cursor.execute("SELECT id, usuario_sistema, gt_usuario FROM credenciales_gt")
for fila in cursor.fetchall():
    print(fila)

cursor.close()
conn.close()