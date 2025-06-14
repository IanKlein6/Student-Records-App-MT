from dotenv import load_dotenv
load_dotenv()

import os

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL"),
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],  # DO NOT include student.py directly
            "default_connection": "default",
        }
    }
}
