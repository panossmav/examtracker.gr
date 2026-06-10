CREATE TABLE exams(
    id SERIAL PRIMARY KEY,
    subj VARCHAR(50) NOT NULL,
    c_date VARCHAR(11) NOT NULL,
    s_name TEXT NOT NULL,
    mark FLOAT NOT NULL
);

CREATE TABLE students(
    id SERIAL PRIMARY KEY,
    s_name TEXT NOT NULL,
    dob VARCHAR(11) NOT NULL
);

CREATE TABLE grade(
    id SERIAL PRIMARY KEY,
    c_name TEXT NOT NULL,
    is_active INTEGER NOT NULL,
    student_amount INTEGER NOT NULL
);

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    pwd TEXT NOT NULL
);