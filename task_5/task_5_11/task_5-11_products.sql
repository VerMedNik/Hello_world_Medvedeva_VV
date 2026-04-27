SELECT * FROM course WHERE credits = 4;
SELECT email FROM student WHERE first_name LIKE '%@Ал';
SELECT first_name FROM student WHERE enrollment_year = 2025 OR enrollment_year = 2024;
SELECT first_name FROM student WHERE NOT enrollment_year = 2025;
SELECT cours_id FROM enrollemnt WHERE grade = 5 OR grade = 4 OR grade = 3;
SELECT * FROM student WHERE (enrollment_year = 2024 AND email LIKE '%ov') OR enrollment_year = 2023;
SELECT * FROM student WHERE first_name = 'Любовь' OR ( enrollment_year = 2025 OR enrollment_year = 2024 AND student_id BETWEEN 1 AND 15);