from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router as endpoints_router
from auth.routes import router as auth_router

app = FastAPI()

# 🟢 Permitir acceso desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://192.168.1.8:5173"],  # Permite solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ✅ Conectar rutas de endpoints y autenticación
app.include_router(endpoints_router)
app.include_router(auth_router)