
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

for tortoise_config import TORTOISE_ORM #adjust path as needed

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False, #Aerich for migrations
    add_exception_handlers=True,
)