CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT,
    class_id INT,
    registration_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_student_class FOREIGN KEY (class_id) 
        REFERENCES classes(class_id) ON DELETE SET NULL
);

CREATE TABLE exams (
    exam_id SERIAL PRIMARY KEY,
    exam_title VARCHAR(150) NOT NULL,
    exam_date DATE DEFAULT CURRENT_DATE,
    subject_id INT NOT NULL,
    class_id INT NOT NULL,
    CONSTRAINT fk_exam_subject FOREIGN KEY (subject_id) 
        REFERENCES subjects(subject_id) ON DELETE CASCADE,
    CONSTRAINT fk_exam_class FOREIGN KEY (class_id) 
        REFERENCES classes(class_id) ON DELETE CASCADE
);

CREATE TABLE grades (
    grade_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    grade_value NUMERIC(4,2) NOT NULL CHECK (grade_value >= 0 AND grade_value <= 20),
    CONSTRAINT fk_grade_student FOREIGN KEY (student_id) 
        REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_grade_exam FOREIGN KEY (exam_id) 
        REFERENCES exams(exam_id) ON DELETE CASCADE,
    CONSTRAINT unique_student_exam UNIQUE (student_id, exam_id)
);