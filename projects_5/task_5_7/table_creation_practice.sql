-- Таблица студентов

CREATE TABLE IF NOT EXISTS students (

    student_id SERIAL PRIMARY KEY,

    first_name VARCHAR(50),

    last_name VARCHAR(50),

    email VARCHAR(100) UNIQUE,

    enrollment_year INT

);



-- Таблица курсов

CREATE TABLE IF NOT EXISTS courses (

    course_id SERIAL PRIMARY KEY,

    course_name VARCHAR(100),

    credits INT

);



-- Таблица связей (многие-ко-многим)

CREATE TABLE IF NOT EXISTS enrollments (

    enrollment_id SERIAL PRIMARY KEY,

    student_id INT REFERENCES students(student_id) ON DELETE CASCADE,

    course_id INT REFERENCES courses(course_id) ON DELETE CASCADE,

    grade INT

);