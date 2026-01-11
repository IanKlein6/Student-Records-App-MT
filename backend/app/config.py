# backend/app/config.py

import os

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL"),
    },
    "apps": {
        "models": {
            "models": [
                "app.models.model_student",
                "app.models.group",
                "app.models.semester",
                "aerich.models",  # required
            ],
            "default_connection": "default",
        },
    },
}
