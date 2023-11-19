CREATE TABLE "user"
(
    id                  serial PRIMARY KEY,
    email_address       email        NOT NULL,
    username            varchar(256) NOT NULL,
    password_hash       varchar(60)  NOT NULL,
    profile_picture_url varchar(2083),
    role                varchar(64)  NOT NULL,
    is_enabled          bool         NOT NULL DEFAULT TRUE,
    created_at          timestamptz  NOT NULL DEFAULT NOW(),
    updated_at          timestamptz  NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX user_email_address
    ON "user" (email_address);

CREATE UNIQUE INDEX user_username
    ON "user" (username);

CREATE TRIGGER user_set_updated_at
    BEFORE UPDATE
    ON "user"
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();
