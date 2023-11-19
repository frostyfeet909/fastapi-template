CREATE TABLE "prediction"
(
    id         serial PRIMARY KEY,
    "user"     int         NOT NULL,
    FOREIGN KEY ("user") REFERENCES "user",
    object_id  int NOT NULL,
    object_created bool,
    created_at timestamptz NOT NULL DEFAULT NOW(),
    updated_at timestamptz NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_prediction_user
    ON "prediction" ("user");

CREATE TRIGGER prediction_set_updated_at
    BEFORE UPDATE
    ON "prediction"
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();
