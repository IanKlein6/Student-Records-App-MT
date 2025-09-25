# backend/app/config.py
TORTOISE_ORM = {
    "connections": {
        # Either DSN string…
        "default": "postgres://postgres:postgres@localhost:5432/student_records",
        # …or explicit engine credentials (either form works)
        # "default": {
        #     "engine": "tortoise.backends.asyncpg",
        #     "credentials": {
        #         "host": "localhost",
        #         "port": 5432,
        #         "user": "postgres",
        #         "password": "postgres",
        #         "database": "student_records",
        #     },
        # },
    },
    "apps": {
        "models": {
            "models": [
                "app.models.student",
                "app.models.group",
                "app.models.semester",
                "aerich.models",   # required
            ],
            "default_connection": "default",
        },
    },
}
