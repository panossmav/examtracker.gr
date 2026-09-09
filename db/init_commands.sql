CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    role TEXT NOT NULL,
    is_active TEXT NOT NULL
);

CREATE TABLE students(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    dob TEXT NOT NULL,
    classroom TEXT,
    subjects TEXT[],
    status TEXT NOT NULL DEFAULT 'active',
    parent TEXT NOT NULL,
    phone TEXT NOT NULL,
);

