CREATE EXTENSION citext;
CREATE DOMAIN email AS citext
  CHECK ( value ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );

CREATE OR REPLACE FUNCTION is_uuid(val text)
    RETURNS boolean AS
$$
BEGIN
    SELECT val::uuid;
    RETURN TRUE;
EXCEPTION WHEN invalid_text_representation THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql
   IMMUTABLE
;

CREATE OR REPLACE FUNCTION set_updated_at()
    RETURNS TRIGGER AS
$$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql'
;
