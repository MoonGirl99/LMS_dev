CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fullname VARCHAR,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lessons (
    lesson_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_courses (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, course_id)
);


CREATE TABLE user_lessons (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    lesson_id INTEGER REFERENCES lessons(lesson_id) ON DELETE CASCADE,
    completed_at TIMESTAMP,
    PRIMARY KEY (user_id, lesson_id)
);



-- Sample Data for the Database

INSERT INTO users (username, email, fullname, hashed_password)
VALUES ('Mahshida', 'mahshid@focusedai.com', 'Mahshid Ahmadi', 'abcd1234$#@%');

INSERT INTO courses (title, description)
VALUES ('Fastapi', 'Introduction of how to work with fastapi');

INSERT INTO lessons (title, content, course_id)
VALUES ('initial setup', 'initial setup for developing a fastapi webapp.', 1);

INSERT INTO lessons (title, content, course_id)
VALUES ('Lesson 2', 'Content for Lesson 2', 1);

INSERT INTO user_courses (user_id, course_id)
VALUES (1, 1);

INSERT INTO user_lessons (user_id, lesson_id, completed_at)
VALUES (1, 1, CURRENT_TIMESTAMP);