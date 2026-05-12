import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers

from .routes import cog, tms_router, colormap_router

app = FastAPI(title="CZGrids TiTiler with custom WMTS CRS")

cors_origins = [origin.strip() for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:8080").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cog.router, prefix="/cog", tags=["Cloud Optimized GeoTIFF"])
app.include_router(tms_router.router, prefix="/cog", tags=["Tiling Schemes"])
app.include_router(colormap_router.router, prefix="/cog", tags=["Colormaps"])


@app.get("/healthz", tags=["Health Check"])
def healthz() -> dict[str, str]:
    return {"status": "ok"}


add_exception_handlers(app, DEFAULT_STATUS_CODES)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)