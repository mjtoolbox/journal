CREATE TABLE Journal (
    id      SERIAL PRIMARY KEY
                    UNIQUE
                    NOT NULL,
    title   TEXT    NOT NULL,
    date    DATE    NOT NULL,
    content TEXT
);