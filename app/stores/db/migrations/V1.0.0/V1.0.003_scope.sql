CREATE TABLE scope
(
    endpoint    varchar(64) NOT NULL,
    action      varchar(64) NOT NULL,
    name        varchar(129) GENERATED ALWAYS AS (endpoint || '.' || action) STORED PRIMARY KEY,
    description text,
    is_enabled  bool        NOT NULL DEFAULT TRUE,
    created_at  timestamptz NOT NULL DEFAULT NOW(),
    updated_at  timestamptz NOT NULL DEFAULT NOW()
);

CREATE TRIGGER scope_set_updated_at
    BEFORE UPDATE
    ON scope
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();


CREATE TABLE role
(
    name        varchar(64) PRIMARY KEY,
    description text,
    is_enabled  bool        NOT NULL DEFAULT TRUE,
    is_default  bool        NOT NULL DEFAULT FALSE,
    created_at  timestamptz NOT NULL DEFAULT NOW(),
    updated_at  timestamptz NOT NULL DEFAULT NOW()
);

CREATE TRIGGER role_set_updated_at
    BEFORE UPDATE
    ON role
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();


CREATE TABLE _scope_role
(
    scope varchar(129),
    role  varchar(64),
    PRIMARY KEY (scope, role),
    FOREIGN KEY (scope) REFERENCES scope ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (role) REFERENCES role ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TRIGGER _scope_role_set_updated_at
    BEFORE UPDATE
    ON _scope_role
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();


CREATE VIEW role_scopes AS
SELECT r.name                                                        AS role,
       ARRAY(SELECT s.name
             FROM scope s
                      INNER JOIN _scope_role sr ON sr.role = r.name) AS scopes
FROM role r;

ALTER TABLE "user"
    ADD CONSTRAINT user_role_fkey FOREIGN KEY (role) REFERENCES role;

INSERT INTO scope (action, endpoint, description)
VALUES ('me', 'user', NULL);

INSERT INTO role (name, description, is_default)
VALUES ('User', 'Free user', TRUE);

INSERT INTO role (name, description)
VALUES ('Subscriber', 'Paying user'),
       ('Admin', 'Admin');


INSERT INTO _scope_role (scope, role)
VALUES ('user.me', 'User'),
       ('user.me', 'Subscriber'),
       ('user.me', 'Admin');