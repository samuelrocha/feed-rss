CREATE TABLE users(
    id INTEGER,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE feeds(
    id INTEGER,
    webportal TEXT NOT NULL,
    link TEXT NOT NULL,
    user_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE categories(
    id INTEGER,
    category TEXT NOT NULL
);

CREATE TABLE errors(
    id INTEGER,
    err TEXT NOT NULL,
    image BLOB
)