from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config
from router.router_register import router_register

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_register,prefix="/main_register",tags=["register"],responses={404: {"description": "Not found"}})

@app.on_event("startup")
async def app_startup():
    config.load_config()

@app.on_event("shutdown")
async def app_shutdown():
    config.close_db_client()

