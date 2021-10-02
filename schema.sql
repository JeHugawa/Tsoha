CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    board_id INTEGER REFERENCES boards
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads,
    poster_id INTEGER REFERENCES users,
    sent TIMESTAMP,
    message TEXT,
    image_path TEXT
);
