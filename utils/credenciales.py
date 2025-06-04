import sqlite3

def obtener_credenciales_gt(usuario_sistema: str):
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT gt_usuario, gt_clave_encriptada FROM credenciales_gt 
        WHERE usuario_sistema = ?
    """, (usuario_sistema,))
    
    fila = cursor.fetchone()
    conexion.close()
    
    if fila:
        return fila[0], fila[1]  # (gt_usuario, clave_plana)
    return None, None