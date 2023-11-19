CREATE TABLE log
(
    id bigserial PRIMARY KEY,
    utc_time timestamptz,
    api_name text,
    operation_name text,
    host_name text,
    http_method text,
    path text,
    resource_id text,
    client_application_name text,
    user_id uuid,
    status_code integer,
    ms_taken integer,
    ms_threshold integer,
    error_code integer,
    error_id uuid,
    correlation_id uuid,
    session_id uuid,
    created_at timestamptz NOT NULL DEFAULT NOW(),
    updated_at timestamptz NOT NULL DEFAULT NOW()
);

CREATE TRIGGER log_set_updated_at
    BEFORE UPDATE
    ON log
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();
