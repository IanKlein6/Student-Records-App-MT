
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise_config import TORTOISE_ORM #adjust path as needed
from app.routers import admin

app = FastAPI()

app.include_router(admin.router) 

@app.get("/")
def read_root():
    return {"message": "Hello World"}


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False, #Aerich for migrations
    add_exception_handlers=True,
)