from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.auth import router as auth_router
from app.routes.products import router as products_router
from app.routes.dashboard import router as dashboard_router
from app.routes.forecasts import router as forecasts_router
from app.routes.alerts import router as alerts_router
from app.routes.orders import router as orders_router
from app.routes.uploads import router as uploads_router

app = FastAPI(
    title="SMART AI FORECASTING API",
    version="1.0.0",
    description="FastAPI backend for AI inventory forecasting and retail insights.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(products_router, prefix="/api", tags=["Products"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
app.include_router(forecasts_router, prefix="/api", tags=["Forecasts"])
app.include_router(alerts_router, prefix="/api", tags=["Alerts"])
app.include_router(orders_router, prefix="/api", tags=["Orders"])
app.include_router(uploads_router, prefix="/api", tags=["Upload & Export"])


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-ai-forecasting-api",
        "project": "HACKINMOTION-RICR-HIM-1105",
    }


@app.get("/")
def root():
    return {
        "message": "SMART AI FORECASTING API is running",
        "docs": "/docs",
        "health": "/health",
    }
