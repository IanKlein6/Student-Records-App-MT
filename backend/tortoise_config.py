import os

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL"),
    },
    "apps": {
        "models": {
            "models": [
                "app.models.student", 
                "aerich.models", 
            ], 
            "default_connection": "default",
        }
    }
}
