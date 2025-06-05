from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from endpoints import router as endpoints_router
from auth.routes import router as auth_router
from auth.database import database  # ⬅️ Importa el objeto de conexión

app = FastAPI()

# 🚀 Conexión a PostgreSQL al iniciar/cerrar
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# ✅ Permitir acceso desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mod-aut-pjic.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD"])
async def leer_root(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    return {"mensaje": "🚀 Backend activo y funcionando"}

# ✅ Conectar rutas de endpoints y autenticación
app.include_router(endpoints_router)
app.include_router(auth_router)