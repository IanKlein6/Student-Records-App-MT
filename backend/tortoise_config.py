import os

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL"),
    },
    "apps": {
        "models": {
            "models": [
                "app.models.student", 
                "app.models.archive_log"
                "aerich.models", 
            ], 
            "default_connection": "default",
        }
    }
}
