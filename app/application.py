from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from app.config.database import Base, engine
from app.routers.main import router

APP_ROOT = Path(__file__).resolve().parent

def get_app() -> FastAPI:
    app = FastAPI(
        title="API Rasoi",
        version="v1",
        description="API created to manage orders in a restaurant.",
        docs_url="/",
        # default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    Base.metadata.create_all(bind=engine)
    # app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")
    app.include_router(router)
    return app
