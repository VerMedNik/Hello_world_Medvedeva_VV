SELECT * FROM enrollemnt WHERE grade BETWEEN 3 AND 5;
SELECT * FROM enrollemnt WHERE (grade BETWEEN 2 AND 5) AND student_id <= 5;
SELECT * FROM enrollemnt WHERE (grade BETWEEN 1 AND 4) AND student_id >= 10;