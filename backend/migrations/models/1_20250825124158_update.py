from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "student" ADD "first_name" VARCHAR(50) NOT NULL;
        ALTER TABLE "student" ADD "status" VARCHAR(8) NOT NULL DEFAULT 'active';
        ALTER TABLE "student" ADD "work_student_potential" VARCHAR(6);
        ALTER TABLE "student" ADD "semester_id" INT;
        ALTER TABLE "student" ADD "attempt_num" INT NOT NULL DEFAULT 0;
        ALTER TABLE "student" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "student" ADD "last_name" VARCHAR(50) NOT NULL;
        ALTER TABLE "student" ADD "notes" VARCHAR(255);
        ALTER TABLE "student" ADD "group_id" INT;
        ALTER TABLE "student" DROP COLUMN "name";
        CREATE TABLE IF NOT EXISTS "group" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
COMMENT ON COLUMN "student"."status" IS 'ACTIVE: active\nPASSED: passed\nFAILED: failed\nARCHIVED: archived';
COMMENT ON COLUMN "student"."work_student_potential" IS 'LOW: low\nMEDIUM: medium\nHIGH: high';
        CREATE TABLE IF NOT EXISTS "semester" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
        ALTER TABLE "student" ADD CONSTRAINT "fk_student_group_81bcd2a3" FOREIGN KEY ("group_id") REFERENCES "group" ("id") ON DELETE CASCADE;
        ALTER TABLE "student" ADD CONSTRAINT "fk_student_semester_294191bf" FOREIGN KEY ("semester_id") REFERENCES "semester" ("id") ON DELETE CASCADE;
        CREATE INDEX IF NOT EXISTS "idx_student_status_9149b4" ON "student" ("status");
        CREATE INDEX IF NOT EXISTS "idx_student_last_na_1a7967" ON "student" ("last_name", "first_name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_student_last_na_1a7967";
        DROP INDEX IF EXISTS "idx_student_status_9149b4";
        ALTER TABLE "student" DROP CONSTRAINT IF EXISTS "fk_student_semester_294191bf";
        ALTER TABLE "student" DROP CONSTRAINT IF EXISTS "fk_student_group_81bcd2a3";
        ALTER TABLE "student" ADD "name" VARCHAR(100) NOT NULL;
        ALTER TABLE "student" DROP COLUMN "first_name";
        ALTER TABLE "student" DROP COLUMN "status";
        ALTER TABLE "student" DROP COLUMN "work_student_potential";
        ALTER TABLE "student" DROP COLUMN "semester_id";
        ALTER TABLE "student" DROP COLUMN "attempt_num";
        ALTER TABLE "student" DROP COLUMN "updated_at";
        ALTER TABLE "student" DROP COLUMN "last_name";
        ALTER TABLE "student" DROP COLUMN "notes";
        ALTER TABLE "student" DROP COLUMN "group_id";
        DROP TABLE IF EXISTS "semester";
        DROP TABLE IF EXISTS "group";"""
