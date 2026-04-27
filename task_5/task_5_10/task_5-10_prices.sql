SELECT * FROM courses ORDER BY credits ASC LIMIT 5;
SELECT student_id FROM enrollments ORDER BY cours_id DESC LIMIT 10;
SELECT student_id FROM enrollments ORDER BY student_id DESC LIMIT 10;
SELECT student_id FROM enrollments ORDER BY student_id ASC LIMIT 51 OFFSET 10;